from fuzzywuzzy import process
from process17LData import *
from processScryfallData import *
import json
from datetime import datetime
import os
import humanize

currentTime = datetime.now()
modified_timestamp = os.path.getmtime("master.json")

# Convert the timestamp to a human-readable date and time
modified_date = currentTime - datetime.fromtimestamp(modified_timestamp)
humanized_date = humanize.naturaldelta(modified_date)

# Print the last modified date
print(f"📈 updated {humanized_date} ago")

with open("master.json") as file:
    master = json.load(file)


# save the previous query
previousQuery = ""

# save if the previous query was top or bottom players
ifPreviousTop = False

# save previous color pair
previousPair = "all"

# process oracle data, card rarity, and card pictures
processScryfallData()

# runs a FuzzyWuzzy program that constantly accepts an input and tells you
# the stats of the card you are looking up. Abbreviations allowed
while True:
    colorWedgeFound = False

    # looks like: "banish, fear, she ambush, shelob child" (in string form) and
    # should get processed into "'Banish from Edoras', 'Fear, Fire, Foes!',
    # 'Shelob's Ambush', 'Shelob, Child of Ungoliant' + their stats
    inputStr: str = input(f"→ ").strip(" ")

    # keep track of if you wanted to query for top players
    topQuery: bool = False

    # keeps track of what color pair I want
    colorPair = "all"

    if inputStr == "":
        print(f'The previous query was "{previousQuery}"')

        if previousQuery == "":
            continue

        inputStr = previousQuery

        topQuery = not ifPreviousTop
        colorPair = previousPair

        print("input string:", inputStr)

    # special command `+` allows you to add to your last query
    if inputStr[0] == "+":
        inputStr = previousQuery + ", " + inputStr[1:]

        topQuery = ifPreviousTop
        colorPair = previousPair

    # special command `-` allows you to subtract from your last query
    if inputStr[0] == "-":
        inputCardNames = inputStr.split(",")

        # copy the list because we'll remove elements from it during iteration
        previousCardNames = previousQuery.split(",")
        previousCopy = previousCardNames.copy()

        choices = master.keys()

        # for every name in input card names, look for it in the previous card
        # names and check for overlap
        for name in inputCardNames:
            closest_match = process.extractOne(name, choices)[0]

            for previousIndex in range(len(previousCopy)):
                previousMatch = process.extractOne(previousCopy[previousIndex], choices)[0]

                if closest_match == previousMatch:
                    previousCardNames.remove(previousCopy[previousIndex])

        inputStr = str.join(", ", previousCardNames)

        topQuery = ifPreviousTop
        colorPair = previousPair

    # checks for a color wedge based on splitting by colon
    colorWedge = inputStr.split(":")[0]

    if inputStr[-1] == ":":
        # process requests for a color wedge / color pair
        if set(colorWedge.lower()) in colorPairAnagrams:
            print("all player color wedge checking")

            colorPairIndex = colorPairAnagrams.index(set(colorWedge.lower()))
            colorPair = colorPairs[colorPairIndex]

            inputStr = previousQuery
            print(inputStr)
            topQuery = ifPreviousTop

            # after both this and the next if block, add a flag
            # that prevents the other block of this type from
            # triggering to avoid removing part of the input
            # string from the query
            colorWedgeFound = True

        if inputStr[:4] == "all:":
            colorPair = "all"

            print(f"querying all cards")

            inputStr = previousQuery
            topQuery = ifPreviousTop

            colorWedgeFound = True

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
        print("querying top players")
        topQuery = True
        inputStr = inputStr[1:]

    # process requests for a color wedge / color pair
    if set(colorWedge.lower()) in colorPairAnagrams and not colorWedgeFound:
        colorPairIndex = colorPairAnagrams.index(set(colorWedge.lower()))
        colorPair = colorPairs[colorPairIndex]

        print(f"querying {colorPair} cards")

        inputStr = inputStr[3:]
        colorPair = colorPair.lower()

    if inputStr[:4] == "all:" and not colorWedgeFound:
        colorPair = "all"

        print(f"querying all cards")

        inputStr = inputStr[4:]
        colorPair = colorPair.lower()

    inputCardNames: List[str] = inputStr.split(",")

    ifPreviousTop = topQuery
    previousPair = colorPair
    previousQuery = inputStr


    if len(inputCardNames) == 1:

        closest_match = process.extractOne(inputStr, choices)[0]

        # get the data from the master JSON
        stats = master[closest_match]["stats"]

        nameToWinrateDict = {}

        print(closest_match)
        print(f'     n alsa {pipe}           GIH {pipe}            OH {pipe}       '
              f'     GD {pipe}     IWD {pipe}  pair')

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
    header = (f'     n alsa {pipe}           GIH {pipe}            OH {pipe}      '
              f'      GD {pipe}     IWD {pipe}  name')

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
        closest_match_blue = f'{ANSI.BLUE.value}{closest_match}{ANSI.RESET.value}'

        stats = master[closest_match]["stats"]
        if topQuery:
            if colorPair in stats["top"].keys():
                winrates = stats["top"][colorPair]
            else:
                print(f"🍓 {closest_match} is not played enough")
                continue
        else:
            if colorPair in stats["all"].keys():
                winrates = stats["all"][colorPair]
            else:
                print(f"🍓 {closest_match} is not played enough")
                continue

        stats = createStatList(winrates, closest_match_blue)

        # retrieve the stat string previously derived and then use it as the
        # value, paired with a key of the name of the card
        statDict[closest_match] = stats

        # retrieve GIH WR from JSON and then pair it with a key of the card's
        # name. This makes sorting easier, and then I can refer back to
        # statDict for the information that I need
        nameToWinrateDict[closest_match] = float(winrates["GIH WR"])

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
