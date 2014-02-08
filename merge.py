# Merge addresses into buildings they intersect with

from fiona import collection
from rtree import index
from shapely.geometry import asShape, Point, LineString

def merge(buildingIn, addressIn):
    addresses = []

    with collection(addressIn, "r") as input:
        for address in input:
            shape = asShape(address['geometry'])
            shape.original = address
            addresses.append(shape)

    # Load and index all buildings.
    buildingIdx = index.Index()
    buildings = []
    with collection(buildingIn, "r") as input:
        for building in input:
            building['shape'] = asShape(building['geometry'])
            building['properties']['addresses'] = []
            buildings.append(building)
            buildingIdx.add(len(buildings) - 1, building['shape'].bounds)

    # Map addresses to buildings.
    for address in addresses:
        for i in buildingIdx.intersection(address.bounds):
            if buildings[i]['shape'].contains(address):
                buildings[i]['properties']['addresses'].append(
                    address.original)

    return {
        'buildings': buildings,
        'index': buildingIdx
    }
