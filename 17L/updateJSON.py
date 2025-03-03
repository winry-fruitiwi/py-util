# this file is for amortization purposes and is an efficient way to run
# the data downloading files quickly. make sure to switch downloadScryfall to
# true whenever a new set rolls out, or the data for the old set will persist.

from getJSONData import *
from dataAggregation import *
from dataCleanup import *
from downloadScryfallData import *

scryfallDownload = False

if scryfallDownload:
    downloadScryfallData()

getJSONData()
cleanJSONData()
aggregateData()
