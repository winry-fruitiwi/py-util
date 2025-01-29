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

# Parameters to Get Access to Different Sets. order of typing
# DSK: 286, dsk, dsk, e%3Aspg+cn≥64+cn≤73, e:dsk, none
# FDN: 281, fdn, fdn, e%3Aspg+cn≥74+cn≤, e:fdn, none

setCode = "fdn"
bonusSheetCode = None
specialGuestQuery = None
theListQuery = None

if setCode == "dsk":
    bonusSheetCode = "dsk"
    # special guest cards
    specialGuestQuery = "e%3Aspg+cn≥64+cn≤73"
    # cards from The List or other seemingly unrelated sets
    theListQuery = 'e:dsk'
    # constant for when additional non-limited cards start
    collectorIDCap = 286
elif setCode == "fdn":
    bonusSheetCode = "fdn"
    specialGuestQuery = "e%3Aspg+cn≥74+cn≤83"
    theListQuery = 'e:fdn'
    collectorIDCap = 281

pipe = "\033[90m|\033[0m"


scryfallAPILink = (f'https://api.scryfall.com/cards/search?q='
                   f'(e:{setCode})+or+(e:{bonusSheetCode})'
                   f'+or+({specialGuestQuery})+or+({theListQuery})')
