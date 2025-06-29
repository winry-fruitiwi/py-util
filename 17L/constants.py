# combinations of all the color pairs in WUBRG order
colorPairs = [
    'wu', 'wb', 'wr', 'wg',
    'ub', 'ur', 'ug',
    'br', 'bg',
    'rg'
]

# a set of each color pair
colorPairAnagrams = [set(pair) for pair in colorPairs]

minGameCountSampleSize = 50

# Parameters to Get Access to Different Sets. order of typing
# DSK: 286, dsk, dsk, e%3Aspg+cn≥64+cn≤73, e:dsk, none
# FDN: 281, fdn, fdn, e%3Aspg+cn≥74+cn≤, e:fdn, none

setCode = "fin"
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

elif setCode == "dft":
    bonusSheetCode = "dft"
    specialGuestQuery = "e:spg+cn≥84+cn≤103"
    theListQuery = 'e:dft'
    collectorIDCap = 291

elif setCode == "tdm":
    bonusSheetCode = "tdm"
    specialGuestQuery = "e:spg+cn≥104+cn≤113"
    theListQuery = 'e:tdm'
    collectorIDCap = 286

elif setCode == "fin":
    bonusSheetCode = "fca"
    specialGuestQuery = "e:fin" # there are no SPG cards for this set
    theListQuery = 'e:fin'
    collectorIDCap = 309

pipe = "\033[90m|\033[0m"


scryfallAPILink = (f'https://api.scryfall.com/cards/search?q='
                   f'(e:{setCode})+or+(e:{bonusSheetCode})'
                   f'+or+({specialGuestQuery})+or+({theListQuery})')
