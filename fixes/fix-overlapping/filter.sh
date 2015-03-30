#!/bin/bash
curl -S --progress-bar "http://osmose.openstreetmap.fr/export/osmose-planet-latest.csv.bz2" > osmose-planet-latest.csv.bz2
gzip -d osmose-planet-latest.csv.bz2
eval "csvgrep -c analyser -r \"osmosis_building_overlaps\" osmose-planet-latest.csv  > world.csv" 
eval "csvgrep -c country -r \"usa_new_york\" world.csv  > nyc.csv"
python csv2shp.py nyc.csv nyc.shp
rm osmose-planet-latest
rm world.csv
rm nyc.csv
