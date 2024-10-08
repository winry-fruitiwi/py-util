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
collectorIDCap = 286

setCode = "dsk"
bonusSheetCode = "dsk"

# special guest cards
specialGuestQuery = "e%3Aspg+cn≥64+cn≤74"
# cards from The List or other seemingly unrelated sets
theListQuery = 'e:dsk'
# cards that aren't special guests or from the list, but still appear in 17L
# cardExceptions = "e%3A"

pipe = "\033[90m|\033[0m"


scryfallAPILink = (f'https://api.scryfall.com/cards/search?q='
                   f'(set:{setCode})+or+(set:{bonusSheetCode})'
                   f'+or+({specialGuestQuery})+or+({theListQuery})')
