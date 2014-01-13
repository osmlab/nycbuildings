from sys import argv
from glob import glob
from merge import merge
import re

def findRanges(buildings):
    onlyRanges = 0 ## Instances where there are only range house numbers in a building
    rangesAndOther = 0
    for building in buildings['data']:
        rangeNum = 0 # House number like "10 - 12"
        total = len(building['properties']['addresses'])
        for address in building['properties']['addresses']:
            if address['properties'][u'HOUSE_NU_2'] is not None:
                rangeNum = rangeNum + 1
            if rangeNum != 0 and rangeNum == total:
                onlyRanges = onlyRanges + 1
            else:
                rangesAndOther = rangesAndOther + 1
    print "%s   %s  %s" % (onlyRanges, rangesAndOther, len(buildings('data')))

# Run conversions. Expects an chunks/addresses-[district id].shp for each
# chunks/buildings-[district id].shp. Optinally convert only one election district.
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
