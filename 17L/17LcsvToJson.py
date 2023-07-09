import csv
import json
import math
import statistics
from typing import List

from fuzzywuzzy import fuzz, process
import Levenshtein

# Path to the CSV file
csv_file_path = 'card-ratings.csv'

# Read the CSV file and store the data in a list of dictionaries
data = []
with open(csv_file_path, 'r', encoding="utf-8-sig") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

# Convert the data to JSON format
json_data = json.dumps(data, indent=4)

# Path to save the resulting JSON file
json_file_path = 'card-ratings.json'

# Save the JSON data to a file
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)

with open(json_file_path, 'r') as file:
    json_data = file.read()

data = json.loads(json_data)

# keeps track of how many real cards are in the set
length = len(data)

# all the GIHWs. The structure is {name: [gihwr, ohwr, alsa, iwd]}. However,
# later the grade and the z-score is added to the beginning of the list.
winrates: dict = {}
winrateSum: int = 0

# iterate through all the JSON data and get the name and GIH winrate
for element in data:
    # next five variables are all strings
    name = element["Name"]

    # GIHW = GIH Winrate
    gihw = element["GIH WR"][:-1]

    # opening hand winrate
    ohwr = element["OH WR"][:-1]

    # average last seen at
    alsa = element["ALSA"]

    # improvement when drawn
    iwd = element["IWD"][:-2]

    # if players haven't played with a card enough for stats to be released,
    # the gihw will be blank. So I have to have a case to handle that.
    if gihw != "":
        gihw = float(gihw)
        winrates[name] = [gihw, ohwr, alsa, iwd]
        winrateSum += gihw
    else:
        winrates[name] = ["not even played enough"]
        length -= 1

# calculate the average of all the gih winrates (already summed up)
μ: float = winrateSum/length
print("μ:", μ)

# find σ, the standard deviation
σ: float = 0

# first, find the variance: Σ((x-μ)²)/N)
for name in winrates:
    wr = winrates[name][0]

    if wr == "not even played enough":
        continue

    deviation: float = (wr - μ)**2

    σ += deviation

σ /= length

# then take the square root of that
σ = math.sqrt(σ)

# find the number of standard deviations each card is away from the mean using
# the equation z=(x-μ)/σ

# to do the above, we need to start with a list of grades and their lower zscore
# bounds. for example, a card with a z-score of 2.25 would be an A+, but any
# card with a z-score below -1.49 (-10 is too low) is really bad.
grades: List[tuple] = [
    ("S ", 2.48),
    ("A+", 2.15),
    ("A ", 1.92),
    ("A-", 1.49),
    ("B+", 1.16),
    ("B ", 0.83),
    ("B-", 0.50),
    ("C+", 0.17),
    ("C ", -0.17),
    ("C-", -0.50),
    ("D+", -0.83),
    ("D ", -1.16),
    ("D-", -1.49),
    ("F ", -10)
]

# grade each card with the z-score equation and the lower bounds of each card
for name in winrates:
    wr = winrates[name][0]

    if wr != "not even played enough":
        z = (wr-μ)/σ

        # calculate which grade the card falls into. For example, "Fear, Fire,
        # Foes!" is an A-, although grades change every once in a while
        cardGrade = ""

        # iterate through each tuple and extract the grade and lower bound
        for i in range(len(grades)):
            grade = grades[i][0]

            # for some reason, the IDE gets mad at me when I don't make sure
            # this is a float, even though it seems like it's supposed to be
            # Theory: F is -10, so it's no longer a float. it's an int
            lowerBound = float(grades[i][1])

            if z > lowerBound:
                cardGrade = grade
                break

        # formats the z-string so that it's much shorter
        zString = str(z)
        neatZ = zString[0:5]

        statList = winrates[name]

        winrates[name] = [cardGrade, neatZ, statList[0], statList[1], statList[2], statList[3]]


# runs a FuzzyWuzzy program that constantly accepts an input and tells you
# the stats of the card you are looking up. Abbreviations allowed
while True:
    # a list of all the winrate keys. Apparently, this is not a list, it's
    # a "_dict_keys" object and I'm not sure how to type that.
    choices = winrates.keys()

    # looks like: "banish, fear, she ambush, shelob child" (in string form) and
    # should get processed into "'Banish from Edoras', 'Fear, Fire, Foes!',
    # 'Shelob's Ambush', 'Shelob, Child of Ungoliant'
    inputCardNames: List[str] = input("→ ").split(",")

    # allows the user to quit the app
    if inputCardNames == ["q"]:
        print("Quitting process...")
        break

    # the header for the stats display
    print(
        f'      zscore   gih     oh      alsa    iwd'
        f'           μ:{μ:.1f}, σ:{σ:.1f}'
        )

    # a dictionary of all the stat strings matched to the GIH winrate of the
    # card. datastructure: gihwr: "grade z-score gih oh alsa iwd name".
    # The name part is WIP
    #
    # 🥝 keying off a non-unique property
    # not having an example of what your data looks like
    # not using f-strings and not typing data, so you constantly have to check
    # having only one window, so you constantly need to scroll
    nameToWinrateDict: dict = {}
    statDict: dict = {}

    for cardName in inputCardNames:
        closest_match = process.extractOne(cardName, choices)[0]

        statList: List[str] = winrates[closest_match]

        # define all the variables inside the stat list, then process
        # them into an f-string
        grade = statList[0]
        zscore = statList[1]
        gih = statList[2]
        oh = statList[3]
        alsa = statList[4]
        # IWD is the most complicated, but even that is just calling the ljust
        # function to add right space padding
        iwd = statList[5].ljust(5)
        stats = f"{grade}    {zscore}    {gih}    {oh}    {alsa}    {iwd}        {closest_match}"

        # retrieve the stat string previously derived and then use it as the
        # value, paired with a key of the name of the card
        statDict[closest_match] = stats

        # retrieve GIH WR from JSON and then pair it with a key of the card's
        # name. This makes sorting easier, and then I can refer back to
        # statDict for the information that I need
        nameToWinrateDict[closest_match] = float(statList[2])

    # Sort based on the value of the statDict. This actually returns a
    # list of floats because it's sorting by the key.
    sorted_data = {k: v for k, v in sorted(nameToWinrateDict.items(),
                                           reverse=True,
                                           key=lambda item: item[1]
                                           )
                   }

    for name in sorted_data:
        print(statDict[name])

print("Process finished")
