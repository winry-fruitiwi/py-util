import csv
import json
import math
import statistics

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

# the all the GIHWs
winrates = {}
winrateSum = 0

# iterate through all the JSON data and get the name and GIH winrate
for element in data:
    name = element["Name"]

    # GIHW = GIH Winrate
    gihw = element["GIH WR"][:-1]

    # if players haven't played with a card enough for stats to be released,
    # the gihw will be blank. So I have to have a case to handle that.
    if gihw != "":
        gihw = float(gihw)
        winrates[name] = gihw
        winrateSum += gihw
    else:
        length -= 1

μ = winrateSum/length
print("μ:", μ)

# find σ, the standard deviation
σ = 0

# first, find the variance: Σ((x-μ)²)/N)
for name in winrates:
    wr = winrates[name]

    deviation = (wr - μ)**2

    σ += deviation

σ /= length

# then take the square root of that
σ = math.sqrt(σ)

# find the number of standard deviations each card is away from the mean using
# the equation z=(x-μ)/σ
grades = [
    ("S ", 2.32),
    ("A+", 1.99),
    ("A ", 1.66),
    ("A-", 1.33),
    ("B+", 0.99),
    ("B ", 0.66),
    ("B-", 0.33),
    ("C+", 0),
    ("C ", -0.33),
    ("C-", -0.66),
    ("D+", -0.99),
    ("D ", -1.33),
    ("D-", -1.66),
    ("F ", -10)
]

for name in winrates:
    wr = winrates[name]
    z = (wr-μ)/σ

    # calculate which grade the card falls into. For example, Elesh Norn Grand
    # Cenobite would be an S
    cardGrade = ""

    # iterate through each tuple and extract the grade and lower bound
    for i in range(len(grades)):
        grade = grades[i][0]

        # for some reason, the IDE gets mad at me when I don't make sure this
        # is a float, even though it seems like it's not supposed to be
        lowerBound = float(grades[i][1])

        if z > lowerBound:
            cardGrade = grade
            break

    # formats the z-string so that it's much shorter
    zString = str(z)
    neatZ = zString[0:5]

    print(cardGrade, wr, neatZ, name)
