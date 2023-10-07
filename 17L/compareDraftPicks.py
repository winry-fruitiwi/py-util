from fuzzywuzzy import process
from process17LData import *
from processScryfallData import *
import json


with open("master.json") as file:
    master = json.load(file)

# runs a FuzzyWuzzy program that constantly accepts an input and tells you
# the stats of the card you are looking up. Abbreviations allowed
while True:
    # looks like: "banish, fear, she ambush, shelob child" (in string form) and
    # should get processed into "'Banish from Edoras', 'Fear, Fire, Foes!',
    # 'Shelob's Ambush', 'Shelob, Child of Ungoliant' + their stats
    inputStr: str = input("→ ")

    # keep track of if you wanted to query for top players
    topQuery: bool = False

    if inputStr == "":
        print("Please input an actual string.")
        continue

    if inputStr == "q":
        break

    # a list of all the winrate keys. Apparently, this is not a list, it's
    # a "_dict_keys" object and I'm not sure how to type that.
    choices = master.keys()

    # if there is an exclamation mark present, then just process
    # the requests for the entire string instead of individually
    # processing stats and oracle requests
    if inputStr[0] == "!":
        closest_match = process.extractOne(inputStr, choices)[0]
        print(cardOracle[closest_match])
        continue

    # process requests for top players
    if inputStr[0] == "~":
        print("querying for top players!")
        topQuery = True

    # checks for a color wedge based on splitting by colon
    colorWedge = inputStr.split(":")[0]

    # keeps track of what color pair I want
    colorPair = "all"

    # process requests for a color wedge / color pair
    if set(colorWedge.lower()) in colorPairAnagrams:
        colorPairIndex = colorPairAnagrams.index(set(colorWedge.lower()))
        colorPair = colorPairs[colorPairIndex]

        print(f"querying for {colorPair.upper()} cards!")

        inputStr = inputStr[3:]
        colorPair = colorPair.lower()

    # process requests for top player data for a color wedge/pair
    elif set(colorWedge[1:].lower()) in colorPairAnagrams:
        print(f"querying for {colorWedge.upper()} cards!")
        inputStr = inputStr[4:]

        colorPair = colorWedge[1:].lower()

    inputCardNames: List[str] = inputStr.split(",")

    if len(inputCardNames) == 1:
        print("you're only looking for 1 card")

        closest_match = process.extractOne(inputStr, choices)[0]

        # get the data from the master JSON
        stats = master[closest_match]["stats"]

        nameToWinrateDict = {}

        print(closest_match)
        print(f'n     alsa |          GIH |           OH |           GD |    IWD  | pair')

        # if I queried for top players, then the winrates used below become
        # the winrate of the top players
        if topQuery:
            winrates = stats["top"]
        else:
            winrates = stats["all"]

        for pair in winrates:
            pairStats = winrates[pair]

            print(createStatList(pairStats, pair.upper()))

        continue

    # the header for the stats display
    header = f'      zscore   gih     oh      alsa    iwd      name'

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

        stats = createStatList(statList, closest_match)

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

print("Quitting...")
