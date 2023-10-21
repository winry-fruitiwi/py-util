import requests
import time
import json
from constants import *

downloadData = input("Do you really want to download the data? yes/no ")

if downloadData.lower() != "yes":
    raise ValueError("You called this file but didn't want to download any data")


def getScryfallData(link):
    # Send a GET requests to the URL
    scryfallData = requests.get(link)

    # Check if the requests was successful (status code 200)
    if scryfallData.status_code == 200:
        # Get the JSON data from the response
        scryfallJSON = scryfallData.json()

        if scryfallJSON["has_more"]:
            time.sleep(1)
            nextPage = getScryfallData(scryfallJSON["next_page"])
            return scryfallJSON["data"] + nextPage

        return scryfallJSON["data"]
    else:
        print("Warning: no data available. Please refrain from using "
              "the '!cardName' command.")


with open(scryfallDataPath, 'w', encoding="utf-8") as scryfall:
    json_data = scryfall.write(json.dumps(getScryfallData(scryfallAPILink)))


def get17LDataIntoFile(url, filePath):
    time.sleep(1)
    # get the 17L data
    response = requests.get(url)

    # if the query was successful, write it into the card rating JSON
    if response.status_code == 200:
        text_content = response.text

        with open(filePath, 'w') as file:
            file.write(text_content)
            print(f"📈 stats for file path {filePath} loaded!")
    else:
        print("Request failed with status code:", response.status_code)


topURL = (f"https://www.17lands.com/card_ratings/data?"
          f"expansion={setCode.upper()}&"
          f"format=PremierDraft&"
          f"user_group=top"
          )


allURL = (f"https://www.17lands.com/card_ratings/data?"
          f"expansion={setCode.upper()}&"
          f"format=PremierDraft&"
          )


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

    get17LDataIntoFile(pairURL, f'requests/all/{pair}-card-ratings.json')
    get17LDataIntoFile(topPairURL, f'requests/top/{pair}-card-ratings.json')


get17LDataIntoFile(topURL, 'requests/top/card-ratings.json')
get17LDataIntoFile(allURL, 'requests/all/card-ratings.json')

print(f"🔮 all stats loaded!")
