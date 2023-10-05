# this file turns all the now streamlined data into one big master.json file
import json
from constants import *
from process17LData import gradeCards, fetchFileData

# first, get data needed
colorPairWinrates = {}
topColorPairWinrates = {}
colorPairGrades = {}
topColorPairGrades = {}

allWinrates = fetchFileData('formatted/all/card-ratings.json')

colorPairWinrates["all"] = fetchFileData('formatted/all/card-ratings.json')
topColorPairWinrates["all"] = fetchFileData('formatted/top/card-ratings.json')

print(f"\n\nall")
colorPairGrades["all"] = gradeCards('formatted/all/card-ratings.json')

print(f"\n\nall top")
topColorPairGrades["all"] = gradeCards('formatted/top/card-ratings.json')

for pair in colorPairs:
    topColorPairWinrates[pair] = fetchFileData(
        f'formatted/top/{pair}-card-ratings.json')
    colorPairWinrates[pair] = fetchFileData(
        f'formatted/all/{pair}-card-ratings.json')

    print(f"\n\ntop {pair}")
    topColorPairGrades[pair] = gradeCards(
        f'formatted/top/{pair}-card-ratings.json')

    print(f"\n\n{pair}")
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
        "stats": {
            "all": {
            },
            "top": {
            }
        }
    }

    for pair in colorPairs:
        try:
            colorWinratesOfAPair = colorPairWinrates[pair][cardName]
            colorGradesOfAPair = colorPairGrades[pair][cardName]

            if colorGradesOfAPair[0] != "not even played enough":
                if colorWinratesOfAPair["GIH WR"] is not None and colorGradesOfAPair is not None:
                    jsonFragment["stats"]["all"][pair.upper()] = {
                        "# OH": colorWinratesOfAPair["# OH"],
                        "OH WR": colorWinratesOfAPair["OH WR"],
                        "# GD": colorWinratesOfAPair["# GD"],
                        "GD WR": colorWinratesOfAPair["GD WR"],
                        "# GIH": colorWinratesOfAPair["# GIH"],
                        "GIH WR": colorWinratesOfAPair["GIH WR"],
                        "IWD": colorWinratesOfAPair["IWD"],
                        "grade": colorGradesOfAPair["grade"],
                        "z-score": colorGradesOfAPair["z-score"]
                    }
        except KeyError as e:
            pass


        try:
            topWinratesOfAPair = topColorPairWinrates[pair][cardName]
            topGradesOfAPair = topColorPairGrades[pair][cardName]

            if topGradesOfAPair[0] != "not even played enough":
                if topWinratesOfAPair["GIH WR"] is not None and topGradesOfAPair is not None:
                    jsonFragment["stats"]["top"][pair.upper()] = {
                        "# OH": topWinratesOfAPair["# OH"],
                        "OH WR": topWinratesOfAPair["OH WR"],
                        "# GD": topWinratesOfAPair["# GD"],
                        "GD WR": topWinratesOfAPair["GD WR"],
                        "# GIH": topWinratesOfAPair["# GIH"],
                        "GIH WR": topWinratesOfAPair["GIH WR"],
                        "IWD": topWinratesOfAPair["IWD"],
                        "grade": topGradesOfAPair["grade"],
                        "z-score": topGradesOfAPair["z-score"]
                    }
        except KeyError or TypeError:
            pass

    masterJSON[cardName] = jsonFragment

with open("master.json", "w") as master:
    json.dump(masterJSON, master)
