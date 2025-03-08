import requests
import time
from constants import *

# downloadData = input("Do you really want to download the data? yes/no ")
#
# if downloadData.lower() != "yes":
#     raise ValueError("You called this file but didn't want to download any data")


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



def getJSONData():
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

        get17LDataIntoFile(pairURL,
                           f'requestFiles/all/{pair}-card-ratings.json')
        get17LDataIntoFile(topPairURL,
                           f'requestFiles/top/{pair}-card-ratings.json')


    get17LDataIntoFile(topURL, 'requestFiles/top/card-ratings.json')
    get17LDataIntoFile(allURL, 'requestFiles/all/card-ratings.json')

    print(f"🔮 all stats loaded!")
