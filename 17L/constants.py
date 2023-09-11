# combinations of all the color pairs in WUBRG order
colorPairs = [
    'w', 'u', 'b', 'r', 'g',
    'wu', 'wb', 'wr', 'wg',
    'ub', 'ur', 'ug',
    'br', 'bg',
    'rg'
]

# a set of each color pair
colorPairAnagrams = [set(pair) for pair in colorPairs]

minGameCountSampleSize = 500

setCode = "woe"
bonusSheetCode = "wot"
