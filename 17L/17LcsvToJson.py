import csv
import requests
import json
import math
import statistics
from typing import List
from fuzzywuzzy import fuzz, process
import Levenshtein
import requests
from constants import *


scryfallDataPath = 'scryfall.json'

# constant for when LTR jumpstart cards start
ltrCollectorIDCap = 281

cardOracle = {}

with open(scryfallDataPath, 'r', encoding="utf-8") as scryfall:
    scryfallData = json.load(scryfall)

# print all the names of each card within the collector ID cap for the set.
# The collector ID cap is when the cards begin to move out of the boosters and
# become cards in special Magic card boxes. We're not concerned about these
# cards.
for card in scryfallData:
    if int(card["collector_number"]) < ltrCollectorIDCap:
        # cardOracle format:
        # Name ManaCost
        # OracleText
        # Power / Toughness
        # FlavorText

        # however, sometimes the power or toughness does not exist, so
        # we need to account for this. (like in the case of instants and
        # sorceries, although some artifacts or vehicles do have power or
        # toughness)
        # the same goes for flavor text

        # handles absence of flavor text
        try:
            flavor_text = card["flavor_text"]
        except KeyError:
            flavor_text = ""

        # handles absence of power/toughness
        try:
            stats = f'{card["power"]}/{card["toughness"]}'
        except KeyError:
            stats = ""


        cardOracle[card["name"]] = (f'{card["name"]}   {card["mana_cost"]}\n'
                                    f'{card["oracle_text"]}\n'
                                    f'{stats}\n'
                                    f'{flavor_text}\n'
                                    )


def process17LJson(json_file_path):
    with open(json_file_path, 'r') as file:
        json_data = file.read()

    data = json.loads(json_data)

    # keeps track of how many real cards are in the set
    length = len(data)

    # all the GIHWs. The structure is {name: [gihwr, ohwr, alsa, iwd]}. However,
    # later the grade and the z-score is added to the beginning of the list.
    winrates: dict = {}
    winrateSum: int = 0

    # iterate through all the JSON data and get the name and GIH winrate
    for element in data:
        # next five variables are all strings
        name = str(element["name"])

        # GIHW = GIH Winrate
        # if there are no instances where a card is ever drawn, then
        # it should be treated as 0 instead of null
        if element["ever_drawn_game_count"] <= minGameCountSampleSize:
            winrates[name] = ["not even played enough"]
            continue

        gihw = str(round(element["ever_drawn_win_rate"] * 100, 1))

        # opening hand winrate
        # if there are no instances where a card is ever drawn, then
        # it should be treated as 0 instead of null
        if element["opening_hand_game_count"] == 0:
            winrates[name] = ["not even played enough"]
            continue

        ohwr = str(round(element["opening_hand_win_rate"] * 100, 1))

        # average last seen at
        alsa = str(round(element["avg_seen"], 2))

        # improvement when drawn

        iwd = str(round(element["drawn_improvement_win_rate"] * 100, 1))

        # if players haven't played with a card enough for stats to be released,
        # the gihw will be blank. So I have to have a case to handle that.
        if (gihw != "") and (ohwr != ""):
            gihw = float(gihw)
            winrates[name] = [gihw, ohwr, alsa, iwd]
            winrateSum += gihw
        else:
            winrates[name] = ["not even played enough"]
            length -= 1

    # calculate the average of all the gih winrates (already summed up)
    μ: float = winrateSum/length

    # find σ, the standard deviation
    σ: float = 0

    # first, find the variance: Σ((x-μ)²)/N)
    for name in winrates:
        wr = winrates[name][0]

        if wr == "not even played enough":
            continue

        deviation: float = (wr - μ)**2

        σ += deviation

    σ /= length

    # then take the square root of that
    σ = math.sqrt(σ)

    # find the number of standard deviations each card is away from the mean using
    # the equation z=(x-μ)/σ

    # to do the above, we need to start with a list of grades and their lower zscore
    # bounds. for example, a card with a z-score of 2.25 would be an A+, but any
    # card with a z-score below -1.49 (-10 is too low) is unplayable.
    grades: List[tuple] = [
        ("S ", 2.48),
        ("A+", 2.15),
        ("A ", 1.92),
        ("A-", 1.49),
        ("B+", 1.16),
        ("B ", 0.83),
        ("B-", 0.50),
        ("C+", 0.17),
        ("C ", -0.17),
        ("C-", -0.50),
        ("D+", -0.83),
        ("D ", -1.16),
        ("D-", -1.49),
        ("F ", -10)
    ]

    # grade each card with the z-score equation and the lower bounds of each card
    for name in winrates:
        wr = winrates[name][0]

        if wr != "not even played enough":
            z = (wr-μ)/σ

            # calculate which grade the card falls into. For example, "Fear, Fire,
            # Foes!" is an A-, although grades change every once in a while
            cardGrade = ""

            # iterate through each tuple and extract the grade and lower bound
            for i in range(len(grades)):
                grade = grades[i][0]

                # for some reason, the IDE gets mad at me when I don't make sure
                # this is a float, even though it seems like it's supposed to be
                # Theory: F is -10, so it's no longer a float. it's an int
                lowerBound = float(grades[i][1])

                if z > lowerBound:
                    cardGrade = grade
                    break

            # formats the z-string so that it's much shorter
            zString = str(z)
            neatZ = zString[0:5]

            statList = winrates[name]

            winrates[name] = [cardGrade,
                              neatZ,
                              statList[0],
                              statList[1],
                              statList[2],
                              statList[3]]

    return winrates


allWinrates = process17LJson('card-ratings.json')
topWinrates = process17LJson('top-card-ratings.json')
colorPairWinrates = {}
topColorPairWinrates = {}

for pair in colorPairs:
    colorPairWinrates[pair] = process17LJson(f'{pair}-card-ratings.json')
    topColorPairWinrates[pair] = process17LJson(f'top-{pair}-card-ratings.json')

# runs a FuzzyWuzzy program that constantly accepts an input and tells you
# the stats of the card you are looking up. Abbreviations allowed
while True:
    # looks like: "banish, fear, she ambush, shelob child" (in string form) and
    # should get processed into "'Banish from Edoras', 'Fear, Fire, Foes!',
    # 'Shelob's Ambush', 'Shelob, Child of Ungoliant' + their stats
    inputStr: str = input("→ ")

    if inputStr == "":
        print("Please input an actual string.")
        continue

    # a list of all the winrate keys. Apparently, this is not a list, it's
    # a "_dict_keys" object and I'm not sure how to type that.
    choices = allWinrates.keys()

    # the winrates is either all the winrates or just the top winrates
    # or any color pair / wedge
    winrates = allWinrates

    # if there is an exclamation mark present, then just process
    # the request for the entire string instead of individually
    # processing stats and oracle requests
    if inputStr[0] == "!":
        closest_match = process.extractOne(inputStr, choices)[0]
        print(cardOracle[closest_match])
        continue

    # process request for top players
    if inputStr[0] == "~":
        print("querying for top players!")
        choices = topWinrates.keys()
        winrates = topWinrates

    # checks for a color wedge based on splitting by colon
    colorWedge = inputStr.split(":")[0]

    # process request for a color wedge / color pair
    if colorWedge.lower() in colorPairs:
        print(f"querying for {colorWedge.upper()} cards!")
        winrates = colorPairWinrates[colorWedge.lower()]
        inputStr = inputStr[3:]

    # process request for top player data for a color wedge/pair
    elif colorWedge[1:].lower() in colorPairs:
        print(f"querying for {colorWedge.upper()} cards!")
        winrates = topColorPairWinrates[colorWedge[1:].lower()]
        inputStr = inputStr[4:]

    inputCardNames: List[str] = inputStr.split(",")

    if len(inputCardNames) == 1:
        print("you're only looking for 1 card")

        closest_match = process.extractOne(inputStr, choices)[0]

        nameToWinrateDict = {}

        print(f'{closest_match}\npair          zscore   gih     oh'
              f'      alsa    iwd')

        for pair in colorPairWinrates:
            pairStats = colorPairWinrates[pair]

            statList: List[str] = pairStats[closest_match]

            if statList[0] == "not even played enough":
                continue

            # define all the variables inside the stat list, then process
            # them into an f-string
            grade = statList[0]
            zscore = statList[1]
            gih = statList[2]
            oh = statList[3]
            # since alsa can't be negative, it has one less padding than iwd
            alsa = statList[4].ljust(4)
            # IWD is the most complicated, but even that is just calling the ljust
            # function to add right space padding
            iwd = statList[5].ljust(5)

            print(f"{pair.upper()}      {grade}    {zscore}    {gih}    {oh}"
                     f"    {alsa}    {iwd}")
        continue

    # allows the user to quit the app
    if inputCardNames == ["q"]:
        print("Quitting process...")
        break

    # the header for the stats display
    header = f'      zscore   gih     oh      alsa    iwd          name'

    # a dictionary of all the stat strings matched to the GIH winrate of the
    # card. datastructure: gihwr: "grade z-score gih oh alsa iwd name".
    # The name part is WIP
    #
    # 🥝 keying off a non-unique property
    # not having an example of what your data looks like
    # not using f-strings and not typing data, so you constantly have to check
    # having only one window, so you constantly need to scroll
    nameToWinrateDict: dict = {}
    statDict: dict = {}

    for cardName in inputCardNames:
        closest_match = process.extractOne(cardName, choices)[0]

        statList: List[str] = winrates[closest_match]

        if statList[0] == "not even played enough":
            print(f"🍓 {closest_match} is not played enough")
            continue

        # define all the variables inside the stat list, then process
        # them into an f-string
        grade = statList[0]
        zscore = statList[1]
        gih = statList[2]
        oh = statList[3]
        # since alsa can't be negative, it has one less padding than iwd
        alsa = statList[4].ljust(4)
        # IWD is the most complicated, but even that is just calling the ljust
        # function to add right space padding
        iwd = statList[5].ljust(5)
        stats = (f"{grade}    {zscore}    {gih}    {oh}"
                 f"    {alsa}    {iwd}        {closest_match}")

        # retrieve the stat string previously derived and then use it as the
        # value, paired with a key of the name of the card
        statDict[closest_match] = stats

        # retrieve GIH WR from JSON and then pair it with a key of the card's
        # name. This makes sorting easier, and then I can refer back to
        # statDict for the information that I need
        nameToWinrateDict[closest_match] = float(statList[2])

    # Sort based on the value of the statDict. This actually returns a
    # list of floats because it's sorting by the key.
    sorted_data = {k: v for k, v in sorted(nameToWinrateDict.items(),
                                           reverse=True,
                                           key=lambda item: item[1]
                                           )
                   }

    print(header)
    for name in sorted_data:
        print(statDict[name])

print("Process finished")
