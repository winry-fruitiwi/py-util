import json
import requests
import time
from constants import *

scryfallDataPath = 'scryfall.json'


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
        print(scryfallData.status_code)


def downloadScryfallData():
    with open(scryfallDataPath, 'w', encoding="utf-8") as scryfall:
        json_data = scryfall.write(json.dumps(getScryfallData(scryfallAPILink)))
        print("🎴Scryfall data found")
