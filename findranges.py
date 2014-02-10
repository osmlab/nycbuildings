# Tally range-style addresses on a per address file level.
from sys import argv
from glob import glob
from merge import merge
import re
from pprint import pprint

def findRanges(buildings):
    def isQueens(housenumber):
        return bool(re.search(r'(\w+-\w+)', housenumber))
    onlyRanges = 0 ## Buildings with only range house numbers
    onlyRangesQueens = 0 ## Buildings with only range house numbers that are queens style
    rangesAndOther = 0 ## Buildings with range numbers and other numbers
    for building in buildings['buildings']:
        rangeNum = 0 # House number like "10 - 12"
        queensRangeNum = 0 # House number like "10-12 - 10-15"
        total = len(building['properties']['addresses'])
        for address in building['properties']['addresses']:
            p = address['properties']
            if p[u'HOUSE_NU_2'] is not None:
                rangeNum += 1
                if isQueens(p[u'HOUSE_NUMB']) and isQueens(p[u'HOUSE_NU_2']):
                    queensRangeNum += 1
        if rangeNum != 0 and rangeNum == total:
            onlyRanges += 1
        elif rangeNum != 0:
            rangesAndOther = rangesAndOther + 1
        if queensRangeNum !=0 and queensRangeNum == total:
            onlyRangesQueens += 1
    print "%s,%s,%s,%s" % (onlyRanges, onlyRangesQueens, rangesAndOther, len(buildings['buildings']))

# Run conversions. Expects an chunks/addresses-[district id].shp for each
# chunks/buildings-[district id].shp. Optinally convert only one election district.
print "# of buildings where all addresses are a range,# of buildings where all addresses are a range and each address is queens-style, # of buildings with both range and non-range addresses,# of all buildings"
if (len(argv) == 2):
    findRanges(merge(
        'chunks/buildings-%s.shp' % argv[1],
        'chunks/addresses-%s.shp' % argv[1]))
else:
    buildingFiles = glob("chunks/buildings-*.shp")
    for buildingFile in buildingFiles:
        matches = re.match('^.*-(\d+)\.shp$', buildingFile).groups(0)
        findRanges(merge(
            buildingFile,
            'chunks/addresses-%s.shp' % matches[0]))
