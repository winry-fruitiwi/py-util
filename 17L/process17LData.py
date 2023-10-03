import json
import math
from typing import List
from constants import *
import statistics


def fetchFileData(json_file_path):
    with open(json_file_path, 'r') as file:
        json_data = file.read()

    return json.loads(json_data)


def gradeCards(json_file_path):
    data = fetchFileData(json_file_path)

    # a list of GIH, OH, and GD winrates
    winrates = {}

    for cardName in data:
        card = data[cardName]

        winrates[cardName] = {
            "OH WR": card["OH WR"],
            "GD WR": card["GD WR"],
            "GIH WR": card["GIH WR"],
        }

    # Extract winrate values into a list while filtering out None values
    ohWRs = [inner_dict["OH WR"] for inner_dict in winrates.values() if
             "OH WR" in inner_dict and inner_dict["OH WR"] is not None]

    # Check if there are valid "b" values before calculating the mean
    if ohWRs:
        mean_oh = statistics.mean(ohWRs)
        stdev_oh = statistics.stdev(ohWRs)
    else:
        print("No OH WR grades found.")
        stdev_oh = 0
        mean_oh = 0

    # Extract winrate values into a list while filtering out None values
    gihWRs = [inner_dict["GIH WR"] for inner_dict in winrates.values() if
              "GIH WR" in inner_dict and inner_dict["GIH WR"] is not None]

    # Check if there are valid "b" values before calculating the mean
    if gihWRs:
        mean_gih = statistics.mean(gihWRs)
        stdev_gih = statistics.stdev(gihWRs)
    else:
        print("No GIH WR grades found.")
        stdev_gih = 0
        mean_gih = 0

    # Extract winrate values into a list while filtering out None values
    gdWRs = [inner_dict["GD WR"] for inner_dict in winrates.values() if
             "GD WR" in inner_dict and inner_dict["GD WR"] is not None]

    # Check if there are valid "b" values before calculating the mean
    if gdWRs:
        mean_gd = statistics.mean(gdWRs)
        stdev_gd = statistics.stdev(gdWRs)
    else:
        print("No GD WR grades found.")
        stdev_gd = 0
        mean_gd = 0

    # find the number of standard deviations each card is away from the mean using
    # the equation z=(x-μ)/σ

    # to do the above, we need to start with a list of grades and their lower zscore
    # bounds. for example, a card with a z-score of 2.25 would be an A+, but any
    # card with a z-score below -1.49 (-10 is too low) is unplayable.
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
        ("F ", -10.0)
    ]

    # the grades of all the cards
    cardGrades = {}

    for cardName in winrates:
        winrateDict = winrates[cardName]

        if (mean_gd != 0) and (stdev_gd != 0):
            # find z-score of gd wr
            wr = winrateDict["GD WR"]

            if wr is not None:
                z = (wr - mean_gd)/stdev_gd

                cardGrade = ""

                for i in range(len(grades)):
                    grade = grades[i][0]

                    # for some reason, the IDE gets mad at me when I don't make sure
                    # this is a float, even though it seems like it's supposed to be
                    # Theory: F is -10, so it's no longer a float. it's an int
                    lowerBound = float(grades[i][1])

                    if z > lowerBound:
                        cardGrade = grade
                        break

                cardGrades[cardName] = {"GD grade": cardGrade,
                                        "GD zscore": z}

        if (mean_gih != 0) and (stdev_gih != 0):
            # find z-score of gd wr
            wr = winrateDict["GIH WR"]

            if wr is not None:
                z = (wr - mean_gih)/stdev_gih

                cardGrade = ""

                for i in range(len(grades)):
                    grade = grades[i][0]

                    # for some reason, the IDE gets mad at me when I don't make sure
                    # this is a float, even though it seems like it's supposed to be
                    # Theory: F is -10, so it's no longer a float. it's an int
                    lowerBound = float(grades[i][1])

                    if z > lowerBound:
                        cardGrade = grade
                        break

                cardGrades[cardName] = {"GIH grade": cardGrade,
                                        "GIH zscore": z}


        if (mean_oh != 0) and (stdev_oh != 0):
            # find z-score of gd wr
            wr = winrateDict["OH WR"]

            if wr is not None:
                z = (wr - mean_oh)/stdev_oh

                cardGrade = ""

                for i in range(len(grades)):
                    grade = grades[i][0]

                    # for some reason, the IDE gets mad at me when I don't make sure
                    # this is a float, even though it seems like it's supposed to be
                    # Theory: F is -10, so it's no longer a float. it's an int
                    lowerBound = float(grades[i][1])

                    if z > lowerBound:
                        cardGrade = grade
                        break

                cardGrades[cardName] = {"OH grade": cardGrade,
                                        "OH zscore": z}


    # # keeps track of how many real cards are in the set
    # length = len(data)
    #
    # # all the GIHWs. The structure is {name: [gihwr, ohwr, alsa, iwd]}. However,
    # # later the grade and the z-score is added to the beginning of the list.
    # winrates: dict = {}
    # winrateSum: int = 0
    #
    # # iterate through all the JSON data and get the name and GIH winrate
    # for name in data:
    #     # next five variables are all strings
    #     element = data[name]
    #
    #     # GIHW = GIH Winrate
    #     # if there are no instances where a card is ever drawn, then
    #     # it should be treated as 0 instead of null
    #     if element["# GIH"] <= minGameCountSampleSize:
    #         winrates[name] = ["not even played enough", 0, 0, 0]
    #         length -= 1
    #         continue
    #
    #     gihw = str(round(element["GIH WR"] * 100, 1))
    #
    #     # opening hand winrate
    #     # if there are no instances where a card is ever drawn, then
    #     # it should be treated as 0 instead of null
    #     if element["# OH"] <= minGameCountSampleSize:
    #         winrates[name] = ["not even played enough", 0, 0, 0]
    #         length -= 1
    #         continue
    #
    #     ohwr = str(round(element["OH WR"] * 100, 1))
    #
    #     # average last seen at
    #     alsa = str(round(element["ALSA"], 2))
    #
    #     # improvement when drawn
    #
    #     iwd = str(round(element["IWD"] * 100, 1))
    #
    #     # if players haven't played with a card enough for stats to be released,
    #     # the gihw will be blank. So I have to have a case to handle that.
    #     if (gihw != "") and (ohwr != ""):
    #         gihw = float(gihw)
    #         winrates[name] = [gihw, ohwr, alsa, iwd]
    #         winrateSum += gihw
    #     else:
    #         winrates[name] = ["not even played enough", 0, 0, 0]
    #         length -= 1
    #
    # # calculate the average of all the gih winrates (already summed up)
    # if length == 0:
    #     print("Hi, top data not available. Path:", json_file_path)
    #     print(winrates)
    #     return
    #
    # μ: float = winrateSum/length
    #
    # # find σ, the standard deviation
    # σ: float = 0
    #
    # # first, find the variance: Σ((x-μ)²)/N)
    # for name in winrates:
    #     wr = winrates[name][0]
    #
    #     if wr == "not even played enough":
    #         continue
    #
    #     deviation: float = (wr - μ)**2
    #
    #     σ += deviation
    #
    # σ /= length
    #
    # # then take the square root of that
    # σ = math.sqrt(σ)
    #
    #
    # # grade each card with the z-score equation and the lower bounds of each card
    # for name in winrates:
    #     wr = winrates[name][0]
    #
    #     if wr != "not even played enough":
    #
    #         if σ == 0:
    #             print("Top data not available. Path:", json_file_path)
    #             return
    #
    #         z = (wr-μ)/σ
    #
    #         # calculate which grade the card falls into. For example, "Fear, Fire,
    #         # Foes!" is an A-, although grades change every once in a while
    #         cardGrade = ""
    #
    #         # iterate through each tuple and extract the grade and lower bound
    #         for i in range(len(grades)):
    #             grade = grades[i][0]
    #
    #             # for some reason, the IDE gets mad at me when I don't make sure
    #             # this is a float, even though it seems like it's supposed to be
    #             # Theory: F is -10, so it's no longer a float. it's an int
    #             lowerBound = float(grades[i][1])
    #
    #             if z > lowerBound:
    #                 cardGrade = grade
    #                 break
    #
    #         # formats the z-string so that it's much shorter
    #         zString = str(z)
    #         neatZ = zString[0:5]
    #
    #         winrates[name] = {"grade": cardGrade,
    #                           "z-score": neatZ
    #                           }
    #
    # return winrates


def createStatList(json):
    # construct a stat string and print it
    # format: statList = [grade, zscore, diff, oh, alsa, iwd]
    # I'm using ljust to make sure that alsa is always 4 chars long, using
    # spaces to pad the right side
    grade = statList[0]
    zscore = statList[1]
    gih = statList[2]
    oh = statList[3]
    alsa = statList[4].ljust(4)
    iwd = statList[5].ljust(5)
    return f"{grade}    {zscore}    {gih}    {oh}" \
           f"    {alsa}    {iwd}    {nameOrCard}"
