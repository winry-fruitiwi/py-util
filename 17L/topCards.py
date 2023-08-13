from processJSON import *
from constants import *

# a file that looks for each archetype and returns the top commons of that
# archetype. Does not count top players.
allWinrates = process17LJson('card-ratings.json')
colorPairWinrates = {}

for pair in colorPairs:
    pairData = process17LJson(f'{pair}-card-ratings.json')
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

        if statList == ["not even played enough"]:
            continue

        grade = statList[0]
        zscore = statList[1]
        gih = statList[2]
        oh = statList[3]
        # since alsa can't be negative, it has one less padding than iwd
        alsa = statList[4].ljust(4)
        # IWD is the most complicated, but even that is just calling the ljust
        # function to add right space padding
        iwd = statList[5].ljust(5)
        print(f"{grade}    {zscore}    {gih}    {oh}"
              f"    {alsa}    {iwd}        {card}")

        cardsPrinted += 1

        # break if I have printed every card
        if cardsPrinted == 10:
            cardsPrinted = 0
            break
