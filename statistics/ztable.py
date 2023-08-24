import scipy.stats as stats
import numpy as np
from scipy.integrate import quad

print("Hello! This program currently takes in a μ, σ, and value and processes"
      " it to make a Z-score for the value.\n")


# takes in a μ, σ, and value and finds its z-score
def findZScore(μ, σ, value):
    # zscore = number of standard deviations away from the mean
    zScore = (value - μ) / σ

    return zScore


def cdfAboveOrBelowZ():
    # gets user input for μ, σ, and value
    μ = float(input("μ: "))
    σ = float(input("σ: "))
    value = float(input("value1: "))

    # Z-score for which you want to find the cumulative probability
    z_score = findZScore(μ, σ, value)

    # Calculate the cumulative probability (area under the curve to the left of z)
    cumulative_prob = stats.norm.cdf(z_score)

    if input("1. above or 2. below?") == "2":
        print("Cumulative Probability:", round(cumulative_prob, 4))
    else:
        print("Cumulative Probability:", 1 - round(cumulative_prob, 4))


def normal_pdf(x, mu, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(
        -((x - mu) ** 2) / (2 * sigma ** 2))


def quadBetweenTwoZs():
    # gets user input for μ, σ, and value
    μ = float(input("μ: "))
    σ = float(input("σ: "))
    valueUpper = float(input("value1: "))
    valueLower = float(input("value1: "))

    # compute the two z-scores based on the two values
    zUpper = findZScore(μ, σ, valueUpper)
    zLower = findZScore(μ, σ, valueLower)

    # Create a lambda function for the PDF with fixed parameters
    pdf_function = lambda x: normal_pdf(x, 0, 1)

    # Integrate the PDF over a certain range using quad()
    result = quad(pdf_function, zUpper, zLower)

    print("Result of integration:", round(result[0], 4))


def ppfPercentileToZ():
    μ = float(input("mean: "))
    σ = float(input("stdev: "))
    percentile = float(input("percentile: "))/100

    z = stats.norm.ppf(percentile)
    print(z * σ + μ)


while True:
    print("1. CDF for area above/below Z")
    print("2. quad for area between two Zs")
    print("3. percentile to value")

    mode = input("→ ")

    match mode:
        case "1":
            cdfAboveOrBelowZ()

        case "2":
            quadBetweenTwoZs()

        case "3":
            ppfPercentileToZ()

        case "q":
            break

        case _:
            print("please choose a valid option")

