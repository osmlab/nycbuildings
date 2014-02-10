# Merge addresses into buildings they intersect with
# Write them to merged/
from fiona import collection
from rtree import index
from shapely.geometry import asShape, Point, LineString
import re
from sys import argv
from glob import glob
from multiprocessing import Pool
import json

def merge(buildingIn, addressIn, mergedOut):
    addresses = []

    with collection(addressIn, "r") as input:
        for address in input:
            shape = asShape(address['geometry'])
            shape.original = address
            addresses.append(shape)

    # Load and index all buildings.
    buildings = []
    buildingShapes = []
    buildingIdx = index.Index()
    with collection(buildingIn, "r") as input:
        for building in input:
            shape = asShape(building['geometry'])
            building['properties']['addresses'] = []
            buildings.append(building)
            buildingShapes.append(shape)
            buildingIdx.add(len(buildings) - 1, shape.bounds)

    # Map addresses to buildings.
    for address in addresses:
        for i in buildingIdx.intersection(address.bounds):
            if buildingShapes[i].contains(address):
                buildings[i]['properties']['addresses'].append(
                    address.original)

    with open(mergedOut, 'w') as outFile:
	    outFile.writelines(json.dumps(buildings, indent=4))
	    print 'Exported ' + mergedOut

def prep(fil3):
    matches = re.match('^.*-(\d+)\.shp$', fil3).groups(0)
    merge(fil3,
        'chunks/addresses-%s.shp' % matches[0],
        'merged/buildings-addresses-%s.geojson' % matches[0])

if __name__ == '__main__':
    # Run merges. Expects an chunks/addresses-[district id].shp for each
    # chunks/buildings-[district id].shp. Optinally convert only one election district.
    if (len(argv) == 2):
        merge('chunks/buildings-%s.shp' % argv[1],
            'chunks/addresses-%s.shp' % argv[1],
            'merged/buildings-addresses-%s.geojson' % argv[1])
    else:
        buildingFiles = glob("chunks/buildings-*.shp")

        pool = Pool()
        pool.map(prep, buildingFiles)
        pool.close()
        pool.join()
