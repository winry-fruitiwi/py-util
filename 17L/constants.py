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
collectorIDCap = 271

setCode = "mkm"
bonusSheetCode = "mkm"

# special guest cards
specialGuestQuery = "e%3Aspg+cn≥19+cn≤28&unique=prints"
# cards from The List
theListQuery = ('e%3Aplst+%28%28%28cn≥+cn≤%29+OR+cn%3A"APC-117"+OR+cn%3A"MH1-21"'
                '+OR+cn%3A"DIS-33"+OR+cn%3A"XLN-91"+OR+cn%3A"C16-47"+OR+cn%3A"SOM-96"+OR+cn%3A"'
                'STX-64"+OR+cn%3A"MH2-191"+OR+cn%3A"ISD-183"+OR+cn%3A"DKA-143"+OR+cn%3A"DST-40"'
                '+OR+cn%3A"MRD-99"+OR+cn%3A"ELD-107"+OR+cn%3A"DKA-4"+OR+cn%3A"M20-167"+OR+cn%3A"'
                'RTR-140"+OR+cn%3A"ONS-89"+OR+cn%3A"WAR-54"+OR+cn%3A"DOM-130"+OR+cn%3A"HOU-149"+'
                'OR+cn%3A"MBS-10"+OR+cn%3A"RAV-277"+OR+cn%3A"2X2-17"+OR+cn%3A"STX-220"+OR+cn%3A'
                '"M14-213"+OR+cn%3A"KLD-221"+OR+cn%3A"ARB-68"+OR+cn%3A"JOU-153"+OR+cn%3A"RNA-182'
                '"+OR+cn%3A"C21-19"+OR+cn%3A"UMA-138"+OR+cn%3A"MH2-46"+OR+cn%3A"VOW-207"+OR+cn%3A'
                '"ONS-272"+OR+cn%3A"UMA-247"+OR+cn%3A"SOM-98"+OR+cn%3A"DDU-50"+OR+cn%3A"CLB-85"'
                '+OR+cn%3A"DIS-173"+OR+cn%3A"SOI-262"%29%29&unique=prints')
# cards that aren't special guests or from the list, but still appear in 17L
cardExceptions = "possibility+storm"

pipe = "\033[90m|\033[0m"
