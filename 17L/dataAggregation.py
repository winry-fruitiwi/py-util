# this file turns all the now streamlined data into one big master.json file
import json
from constants import *
from process17LData import process17LJson

# first, get data needed
allWinrates = process17LJson('formatted/all/card-ratings.json')
topWinrates = process17LJson('formatted/top/card-ratings.json')
colorPairWinrates = {}
topColorPairWinrates = {}

for pair in colorPairs:
    colorPairWinrates[pair] = process17LJson(
        f'formatted/all/{pair}-card-ratings.json')
    topColorPairWinrates[pair] = process17LJson(
        f'formatted/top/{pair}-card-ratings.json')

masterJSON = {}

# then, iterate through each card
for cardName in allWinrates:
    card = allWinrates[cardName]
    # ideal segment of master JSON:
    # {
    #   "name": {
    #     "color": ""
    #     "rarity": ""
    #     "oracle": ""
    #     "stats": {
    #       "all": {
    #         "colorPair": {
    #            "..."
    #         }
    #       }
    #       "top": {
    #         "colorPair": {
    #            "..."
    #         }
    #       }
    #       "..."
    #     }
    #   }
    # }

    jsonFragment = {
        "color": card["color"],
        "rarity": card["rarity"],
        "stats": {
            "all": {
            },
            "top": {
            }
        }
    }

    for pair in colorPairs:
        colorWinrates = colorPairWinrates[pair][cardName]
        topWinrates = topColorPairWinrates[pair][cardName]

        jsonFragment["stats"]["all"][pair] = {
            "# OH": colorWinrates["# OH"],
            "OH WR": colorWinrates["OH WR"],
            "# GD": colorWinrates["# GD"],
            "GD WR": colorWinrates["GD WR"],
            "# GIH": colorWinrates["# GIH"],
            "GIH WR": colorWinrates["GIH WR"],
            "IWD": colorWinrates["IWD"]
        }

        jsonFragment["stats"]["top"][pair] = {
            "# OH": topWinrates["# OH"],
            "OH WR": topWinrates["OH WR"],
            "# GD": topWinrates["# GD"],
            "GD WR": topWinrates["GD WR"],
            "# GIH": topWinrates["# GIH"],
            "GIH WR": topWinrates["GIH WR"],
            "IWD": topWinrates["IWD"]
        }

    masterJSON[cardName] = jsonFragment
