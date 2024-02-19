import requests
import time
import json
from constants import *

# initialize the scryfall API link and pull the data from the website
scryfallAPILink = (f'https://api.scryfall.com/cards/search?q=set%3A{setCode}+or+set%3A{setCode}+or+(set%3Aplst+((('
                   f'cn≥+cn≤)+OR+cn%3A"APC-117"+OR+cn%3A"MH1-21"+OR+cn%3A"DIS-33"+OR+cn%3A"XLN-91"+OR+cn%3A"C16-47"+OR+cn%3A"SOM-96"+OR+cn%3A"STX-64"+OR+cn%3A"MH2-191"+OR+cn%3A"ISD-183"+OR+cn%3A"DKA-143"+OR+cn%3A"DST-40"+OR+cn%3A"MRD-99"+OR+cn%3A"ELD-107"+OR+cn%3A"DKA-4"+OR+cn%3A"M20-167"+OR+cn%3A"RTR-140"+OR+cn%3A"ONS-89"+OR+cn%3A"WAR-54"+OR+cn%3A"DOM-130"+OR+cn%3A"HOU-149"+OR+cn%3A"MBS-10"+OR+cn%3A"RAV-277"+OR+cn%3A"2X2-17"+OR+cn%3A"STX-220"+OR+cn%3A"M14-213"+OR+cn%3A"KLD-221"+OR+cn%3A"ARB-68"+OR+cn%3A"JOU-153"+OR+cn%3A"RNA-182"+OR+cn%3A"C21-19"+OR+cn%3A"UMA-138"+OR+cn%3A"MH2-46"+OR+cn%3A"VOW-207"+OR+cn%3A"ONS-272"+OR+cn%3A"UMA-247"+OR+cn%3A"SOM-98"+OR+cn%3A"DDU-50"+OR+cn%3A"CLB-85"+OR+cn%3A"DIS-173"+OR+cn%3A"SOI-262")))')
scryfallDataPath = 'scryfall.json'

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
