from sys import argv
from glob import glob
from merge import merge
from pprint import pprint
import re

def findRanges(buildings):
    for building in buildings['data']:
        pprint(building['properties'])

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
