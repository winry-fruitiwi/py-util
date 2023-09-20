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
        colorWinratesOfAPair = colorPairWinrates[pair][cardName]
        topWinratesOfAPair = topColorPairWinrates[pair][cardName]

        if colorWinratesOfAPair["GIH WR"] is not None:
            jsonFragment["stats"]["all"][pair.upper()] = {
                "# OH": colorWinratesOfAPair["# OH"],
                "OH WR": colorWinratesOfAPair["OH WR"],
                "# GD": colorWinratesOfAPair["# GD"],
                "GD WR": colorWinratesOfAPair["GD WR"],
                "# GIH": colorWinratesOfAPair["# GIH"],
                "GIH WR": colorWinratesOfAPair["GIH WR"],
                "IWD": colorWinratesOfAPair["IWD"]
            }

        if topWinratesOfAPair["GIH WR"] is not None:
            jsonFragment["stats"]["top"][pair.upper()] = {
                "# OH": topWinratesOfAPair["# OH"],
                "OH WR": topWinratesOfAPair["OH WR"],
                "# GD": topWinratesOfAPair["# GD"],
                "GD WR": topWinratesOfAPair["GD WR"],
                "# GIH": topWinratesOfAPair["# GIH"],
                "GIH WR": topWinratesOfAPair["GIH WR"],
                "IWD": topWinratesOfAPair["IWD"]
            }

    allColorWinrates = allWinrates[cardName]
    allTopWinrates = topWinrates[cardName]

    if allColorWinrates["GIH WR"] is not None:
        jsonFragment["stats"]["all"]["all"] = {
            "# OH": allColorWinrates["# OH"],
            "OH WR": allColorWinrates["OH WR"],
            "# GD": allColorWinrates["# GD"],
            "GD WR": allColorWinrates["GD WR"],
            "# GIH": allColorWinrates["# GIH"],
            "GIH WR": allColorWinrates["GIH WR"],
            "IWD": allColorWinrates["IWD"]
        }

    if allTopWinrates["GIH WR"] is not None:
        jsonFragment["stats"]["top"]["all"] = {
            "# OH": allTopWinrates["# OH"],
            "OH WR": allTopWinrates["OH WR"],
            "# GD": allTopWinrates["# GD"],
            "GD WR": allTopWinrates["GD WR"],
            "# GIH": allTopWinrates["# GIH"],
            "GIH WR": allTopWinrates["GIH WR"],
            "IWD": allTopWinrates["IWD"]
        }

    masterJSON[cardName] = jsonFragment

with open("master.json", "w") as master:
    json.dump(masterJSON, master)
