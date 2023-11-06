# this file turns all the now streamlined data into one big master.json file
import json
from constants import *
from process17LData import gradeCards, fetchFileData
from processScryfallData import *
import requests

# first, get data needed
colorPairWinrates = {}
topColorPairWinrates = {}
colorPairGrades = {}
topColorPairGrades = {}

allWinrates = fetchFileData('formatted/all/card-ratings.json')

colorPairWinrates["all"] = fetchFileData('formatted/all/card-ratings.json')
topColorPairWinrates["all"] = fetchFileData('formatted/top/card-ratings.json')

colorPairGrades["all"] = gradeCards('formatted/all/card-ratings.json')

topColorPairGrades["all"] = gradeCards('formatted/top/card-ratings.json')

for pair in colorPairs:
    topColorPairWinrates[pair] = fetchFileData(
        f'formatted/top/{pair}-card-ratings.json')
    colorPairWinrates[pair] = fetchFileData(
        f'formatted/all/{pair}-card-ratings.json')

    topColorPairGrades[pair] = gradeCards(
        f'formatted/top/{pair}-card-ratings.json')

    colorPairGrades[pair] = gradeCards(
        f'formatted/all/{pair}-card-ratings.json')

with open("test.json", "w") as file:
    json.dump(colorPairGrades, file)

masterJSON = {}

colorPairs.append("all")

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
        "png": cardPNGs[cardName],
        "stats": {
            "all": {
            },
            "top": {
            }
        }
    }

    # iterate through each color pair, find the grades, and then construct a
    # JSON fragment of winrates and grades for each winrate
    for pair in colorPairs:
        colorWinratesOfAPair = colorPairWinrates[pair][cardName]
        colorGradesOfAPair = colorPairGrades[pair][cardName]

        if ((colorWinratesOfAPair["OH WR"] is not None) and
            (colorWinratesOfAPair["GD WR"] is not None) and
            (colorWinratesOfAPair["GIH WR"] is not None)):
            jsonFragment["stats"]["all"][pair] = {
                "# OH": colorWinratesOfAPair["# OH"],
                "OH WR": colorWinratesOfAPair["OH WR"],
                "# GD": colorWinratesOfAPair["# GD"],
                "GD WR": colorWinratesOfAPair["GD WR"],
                "# GIH": colorWinratesOfAPair["# GIH"],
                "GIH WR": colorWinratesOfAPair["GIH WR"],
                "IWD": colorWinratesOfAPair["IWD"],
                "ALSA": colorWinratesOfAPair["ALSA"]
            }
            jsonFragment["stats"]["all"][pair].update(colorGradesOfAPair)


        topWinratesOfAPair = topColorPairWinrates[pair][cardName]
        topGradesOfAPair = topColorPairGrades[pair][cardName]

        if ((topWinratesOfAPair["OH WR"] is not None) and
            (topWinratesOfAPair["GD WR"] is not None) and
            (topWinratesOfAPair["GIH WR"] is not None)):
            jsonFragment["stats"]["top"][pair] = {
                "# OH": topWinratesOfAPair["# OH"],
                "OH WR": topWinratesOfAPair["OH WR"],
                "# GD": topWinratesOfAPair["# GD"],
                "GD WR": topWinratesOfAPair["GD WR"],
                "# GIH": topWinratesOfAPair["# GIH"],
                "GIH WR": topWinratesOfAPair["GIH WR"],
                "IWD": topWinratesOfAPair["IWD"],
                "ALSA": topWinratesOfAPair["ALSA"]
            }
            jsonFragment["stats"]["top"][pair].update(topGradesOfAPair)

    masterJSON[cardName] = jsonFragment

with open("master.json", "w") as master:
    json.dump(masterJSON, master)
