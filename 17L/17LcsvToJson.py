import csv
import json
import math
import statistics

# Path to the CSV file
csv_file_path = 'card-ratings-2023-06-20.csv'

# Read the CSV file and store the data in a list of dictionaries
data = []
with open(csv_file_path, 'r', encoding="utf-8-sig") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

# Convert the data to JSON format
json_data = json.dumps(data, indent=4)

# Path to save the resulting JSON file
json_file_path = 'card-ratings-2023-06-20.json'

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
gradeDict = {
    "S": 2.16,
    "A": 1.83,
    "B+": 1.49,
    "B": 1.06,
    "B-": 0.83,
    "C+": 0,
    "C": -0.83,
    "C-": -1.06,
    "D+": -1.49,
    "D": -1.83,
    "D-": -2.16,
    "F": -10
}

for name in winrates:
    wr = winrates[name]
    z = (wr-μ)/σ

    print(wr, z, name)
