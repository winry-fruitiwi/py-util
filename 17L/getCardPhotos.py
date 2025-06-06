from processScryfallData import *
from process17LData import *
import requests
processScryfallData()
print(cardPNGs)

masterJSON = fetchFileData("master.json")

for cardName in masterJSON:
    # Replace this URL with the image URL you want to download
    try:
        image_url = cardPNGs[cardName]
    except KeyError:
        # this means that the card is probably double-faced
        splitCardFrontName = cardName.split(" // ")[0]
        image_url = cardPNGs[splitCardFrontName]
        cardName = splitCardFrontName

    # Send an HTTP GET request to the image URL
    response = requests.get(image_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the content of the response (the image binary data)
        image_data = response.content

        # Specify the file path where you want to save the image
        file_path = f'cardImages/{cardName}.png'

        # Open the file in binary write mode and write the image data to it
        with open(file_path, 'wb+') as file:
            file.write(image_data)

        print(f"Image downloaded and saved to {file_path}")
    else:
        print(
            f"Failed to download the image. Card name: {cardName}")
