from sys import argv
import glob
import csv
from shapely.geometry import Point, mapping
from fiona import collection

path = ''
f_csv = path + argv[1]
f_shp = path + argv[2]
schema = { 'geometry': 'Point', 'properties': {'country': 'str', 'elems': 'str', 'class': 'int', 'subclass': 'int', 'item': 'int' } }
with collection(
    f_shp, "w", "ESRI Shapefile", schema) as output:
    with open(f_csv, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            point = Point(float(row['lon']), float(row['lat']))
            output.write({
                'properties': {
                    'country':row['country'],
                    'elems':row['elems'],
                    'class':row['class'],
                    'subclass':row['subclass'],
                    'item':row['item']
                },
                'geometry': mapping(point)
            })

