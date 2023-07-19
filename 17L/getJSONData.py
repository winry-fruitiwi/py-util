import requests
import time


# initialize the scryfall API link and pull the data from the website
setCode = "ltr"
scryfallAPILink = f"https://api.scryfall.com/cards/search?q=set:{setCode}"
scryfallDataPath = 'scryfall.json'


def getScryfallData(link):
    # Send a GET request to the URL
    scryfallData = requests.get(link)

    # Check if the request was successful (status code 200)
    if scryfallData.status_code == 200:
        # Get the JSON data from the response
        scryfallJSON = scryfallData.json()

        if scryfallJSON["has_more"]:
            time.sleep(1)
            nextPage = getScryfallData(scryfallJSON["next_page"])
            return scryfallJSON["data"] + nextPage

        return scryfallJSON["data"]
    else:
        print("Warning: no Scryfall data available. Please refrain from using "
              "the '!cardName' command.")


with open(scryfallDataPath, 'w', encoding="utf-8") as scryfall:
    json_data = scryfall.write(str(getScryfallData(scryfallAPILink)))


url = (f"https://www.17lands.com/card_ratings/data?"
       f"expansion=LTR&"
       f"format=PremierDraft&"
       f"start_date=2023-06-20&"
       f"end_date=2023-07-17"
       )

# get the 17L data
response = requests.get(url)

# if the query was successful, write it into the card rating JSON
if response.status_code == 200:
    text_content = response.text
    print(text_content)

    json_file_path = 'card-ratings.json'

    with open(json_file_path, 'w') as file:
        json_data = file.write(text_content)
else:
    print("Request failed with status code:", response.status_code)
