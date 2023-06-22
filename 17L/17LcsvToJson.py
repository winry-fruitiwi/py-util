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

# the sum of all the GIHWs
winrates = []

# iterate through all the JSON data and get the name and GIH winrate
for element in data:
    name = element["Name"]

    # GIHW = GIH Winrate
    gihw = element["GIH WR"][:-1]

    # if players haven't played with a card enough for stats to be released,
    # the gihw will be blank. So I have to have a case to handle that.
    if gihw != "":
        gihw = float(gihw)
        winrates.append(gihw)
    else:
        gihw = "so bad it's not played:"
        length -= 1

    print(gihw, name)

μ = sum(winrates)/length
print("μ:", μ)

# find σ, the standard deviation
σ = 0
for wr in winrates:
    deviation = wr - μ

    # preserve the negativity of the deviation
    if deviation < 0:
        deviation *= -deviation
    else:
        deviation *= deviation

    σ += deviation

σ = math.sqrt(σ)

print("σ:", σ)

lib_μ = statistics.mean(winrates)
lib_σ = statistics.stdev(winrates)

print(lib_μ)
print(lib_σ)
