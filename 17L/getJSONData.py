import requests

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
