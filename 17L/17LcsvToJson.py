import csv
import requests
import json
import math
import statistics
from typing import List
from fuzzywuzzy import fuzz, process
import Levenshtein
import requests
import time


# initialize the scryfall API link and pull the data from the website
setCode = "ltr"
# constant for when LTR jumpstart cards start
ltrCollectorIDCap = 281
scryfallAPILink = f"https://api.scryfall.com/cards/search?q=set:{setCode}"


def getScryfallData(link):
    # Send a GET request to the URL
    response = requests.get(link)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the JSON data from the response
        scryfallJSON = response.json()

        if scryfallJSON["has_more"]:
            time.sleep(1)
            nextPage = getScryfallData(scryfallJSON["next_page"])
            return scryfallJSON["data"] + nextPage

        return scryfallJSON["data"]
    else:
        print("Warning: no Scryfall data available. Please refrain from using "
              "the '!cardName' command.")



scryfallData = getScryfallData(scryfallAPILink)
cardOracle = {}

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

json_file_path = 'card-ratings.json'

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
    gihw = str(round(element["ever_drawn_win_rate"] * 100, 1))

    # opening hand winrate
    ohwr = str(round(element["opening_hand_win_rate"] * 100, 1))

    # average last seen at
    alsa = str(round(element["avg_seen"], 2))

    # improvement when drawn
    iwd = str(round(element["drawn_improvement_win_rate"] * 100, 1))

    # if players haven't played with a card enough for stats to be released,
    # the gihw will be blank. So I have to have a case to handle that.
    if gihw != "":
        gihw = float(gihw)
        winrates[name] = [gihw, ohwr, alsa, iwd]
        winrateSum += gihw
    else:
        winrates[name] = ["not even played enough"]
        length -= 1

# calculate the average of all the gih winrates (already summed up)
μ: float = winrateSum/length
print("μ:", μ)

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
# card with a z-score below -1.49 (-10 is too low) is really bad.
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

        winrates[name] = [cardGrade, neatZ, statList[0], statList[1], statList[2], statList[3]]


# runs a FuzzyWuzzy program that constantly accepts an input and tells you
# the stats of the card you are looking up. Abbreviations allowed
while True:
    # a list of all the winrate keys. Apparently, this is not a list, it's
    # a "_dict_keys" object and I'm not sure how to type that.
    choices = winrates.keys()

    # looks like: "banish, fear, she ambush, shelob child" (in string form) and
    # should get processed into "'Banish from Edoras', 'Fear, Fire, Foes!',
    # 'Shelob's Ambush', 'Shelob, Child of Ungoliant'
    inputStr: str = input("→ ")

    # if there is an exclamation mark present, then just process
    # the request for the entire string instead of individually
    # processing stats and oracle requests
    if inputStr[0] == "!":
        closest_match = process.extractOne(inputStr, choices)[0]
        print(cardOracle[closest_match])
        continue

    inputCardNames: List[str] = inputStr.split(",")

    # allows the user to quit the app
    if inputCardNames == ["q"]:
        print("Quitting process...")
        break

    # the header for the stats display
    print(
        f'      zscore   gih     oh      alsa    iwd'
        f'           μ:{μ:.1f}, σ:{σ:.1f}'
        )

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

        # define all the variables inside the stat list, then process
        # them into an f-string
        grade = statList[0]
        zscore = statList[1]
        gih = statList[2]
        oh = statList[3]
        alsa = statList[4]
        # IWD is the most complicated, but even that is just calling the ljust
        # function to add right space padding
        iwd = statList[5].ljust(5)
        stats = f"{grade}    {zscore}    {gih}    {oh}    {alsa}    {iwd}        {closest_match}"

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

    for name in sorted_data:
        print(statDict[name])

print("Process finished")
