import json
from constants import *


# this function operates on 17L archetype data and makes it more
# concise, removing sideboard game count data and adding 17L attribute
# names for keys like ALSA instead of average_last_seen_at.
def streamline17LJSON(fileToOpen, fileToWrite):
    # initialize a dictionary that will later be turned back into JSON
    formattedFile = {}

    # open the file at the file path and format it
    with open(fileToOpen, "r") as file:
        json_data = file.read()

    data = json.loads(json_data)

    for cardJSON in data:
        streamlinedData = {
                "# OH": cardJSON["opening_hand_game_count"],
                "OH WR": cardJSON["opening_hand_win_rate"],
                "# GD": cardJSON["drawn_game_count"],
                "GD WR": cardJSON["drawn_win_rate"],
                "# GIH": cardJSON["ever_drawn_game_count"],
                "GIH WR": cardJSON["ever_drawn_win_rate"],
                "IWD": cardJSON["drawn_improvement_win_rate"],
                "name": cardJSON["name"],
                "color": cardJSON["color"],
                "rarity": cardJSON["rarity"]
        }

        formattedFile[cardJSON["name"]] = streamlinedData

    with open(fileToWrite, "w") as file:
        json.dump(formattedFile, file)


for pair in colorPairs:
    pairURL = (f"https://www.17lands.com/card_ratings/data?"
               f"expansion={setCode.upper()}&"
               f"format=PremierDraft&"
               f"colors={pair}"
               )

    topPairURL = (f"https://www.17lands.com/card_ratings/data?"
                  f"expansion={setCode.upper()}&"
                  f"format=PremierDraft&"
                  f"colors={pair}&"
                  f"user_group=top"
                  )

    streamline17LJSON(f'requests/all/{pair}-card-ratings.json', f'formatted/all/{pair}-card-ratings.json')
    streamline17LJSON(f'requests/top/{pair}-card-ratings.json', f'formatted/top/{pair}-card-ratings.json')


streamline17LJSON('requests/top/card-ratings.json', 'formatted/top/card-ratings.json')
streamline17LJSON('requests/all/card-ratings.json', 'formatted/all/card-ratings.json')

print("🎏 all stats streamlined!")
