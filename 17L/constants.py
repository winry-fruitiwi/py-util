# combinations of all the color pairs in WUBRG order
colorPairs = [
    'wu', 'wb', 'wr', 'wg',
    'ub', 'ur', 'ug',
    'br', 'bg',
    'rg'
]

# a set of each color pair
colorPairAnagrams = [set(pair) for pair in colorPairs]

minGameCountSampleSize = 500

# constant for when jumpstart cards start
collectorIDCap = 276

setCode = "otj"
bonusSheetCode = "otp"

# special guest cards
specialGuestQuery = "e%3Aspg+cn≥29+cn≤38"
# cards from The List
theListQuery = 'e%3Abig+cn≥1+cn≤30'
# cards that aren't special guests or from the list, but still appear in 17L
# cardExceptions = "(possibilitystorm)+or+(evolutionaryleap)+or+(smugglerscopter)"

pipe = "\033[90m|\033[0m"


scryfallAPILink = (f'https://api.scryfall.com/cards/search?q='
                   f'(set:{setCode})+or+(set:{bonusSheetCode})'
                   f'+or+({specialGuestQuery})+or+({theListQuery})')
