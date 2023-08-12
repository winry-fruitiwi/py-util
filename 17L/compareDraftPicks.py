from fuzzywuzzy import process
from processJSON import *
from processScryfallData import *


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

    # keep track if you wanted to query for top players
    topQuery: bool = False

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
        topQuery = True

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

        # if I queried for top players, then the winrates used below become
        # the winrate of the top players
        if topQuery:
            winrates = topColorPairWinrates
        else:
            winrates = colorPairWinrates

        for pair in winrates:
            pairStats = winrates[pair]

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
