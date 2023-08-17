from process17LData import *
from processScryfallData import *
from constants import *

# a file that looks for each archetype and returns the top commons of that
# archetype. Does not count top players.
allWinrates = process17LJson('card-ratings.json')
colorPairWinrates = {}

for pair in colorPairs:
    pairData = process17LJson(f'{pair}-card-ratings.json')
    pairData = sorted_dict = {key: value for key, value in
                              sorted(pairData.items(),
                                     key=lambda x: x[1][2],
                                     reverse=True)
                              }
    colorPairWinrates[pair] = pairData

# number of cards to print for each color pair in upcoming loop
numCardsToPrint = 10

# cards printed in upcoming loop
cardsPrinted = 0

# print all the top cards. TODO: currently printing unsorted dataset
for color in colorPairWinrates:
    colorData = colorPairWinrates[color]
    print(f"\n\n{color.upper()}\n")
    for card in colorData:
        statList = colorData[card]

        if (statList[0] == "not even played enough" or
            rarityOfCards[card] == "rare" or
            rarityOfCards[card] == "mythic"
            ):
            continue

        createStatList(statList, card)

        cardsPrinted += 1

        # break if I have printed every card
        if cardsPrinted == 10:
            cardsPrinted = 0
            break
