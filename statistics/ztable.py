print("Hello! This program currently takes in a μ, σ, and value and processes"
      " it to make a Z-score for the value.\n")


# takes in a μ, σ, and value and finds its z-score
def findZScore(μ, σ, value):
    # zscore = number of standard deviations away from the mean
    zScore = (value-μ)/σ

    return zScore


# gets user input for μ, σ, and value
mean = float(input("μ: "))
stdev = float(input("σ: "))
val = float(input("value: "))

print("Z-score:", findZScore(mean, stdev, val))
