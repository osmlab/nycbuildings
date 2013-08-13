all: buildings/buildings.shp addresses/addresses.shp districts/districts.shp chunks osm

clean:
	rm -f BUILDING_7_25_13.zip
	rm -f NYC_AddressPoint.zip
	rm -f nyedwi_13a.zip

BUILDING_7_25_13.zip:
	curl -L "https://dl.dropboxusercontent.com/u/479174/NYC/BUILDING_7_25_13.zip" -o BUILDING_7_25_13.zip

NYC_AddressPoint.zip:
	curl -L "https://dl.dropboxusercontent.com/u/479174/NYC/NYC_AddressPoint.zip" -o NYC_AddressPoint.zip

nyedwi_13a.zip:
	curl -L "http://www.nyc.gov/html/dcp/download/bytes/nyedwi_13a.zip" -o nyedwi_13a.zip

buildings: BUILDING_7_25_13.zip
	unzip BUILDING_7_25_13.zip -d buildings

addresses: NYC_AddressPoint.zip
	unzip NYC_AddressPoint.zip -d addresses

districts: nyedwi_13a.zip
	unzip -d districts -j nyedwi_13a.zip

buildings/buildings.shp: buildings
	rm -f buildings/buildings.*
	ogr2ogr -simplify 0.2 -t_srs EPSG:4326 -overwrite buildings/buildings.shp buildings/BUILDING_7_25_13.shp

addresses/addresses.shp: addresses
	rm -f addresses/addresses.*
	ogr2ogr -t_srs EPSG:4326 -overwrite addresses/addresses.shp addresses/NYC_AddressPoint.shp

districts/districts.shp: districts
	rm -f districts/districts.*
	ogr2ogr -simplify 20 -t_srs EPSG:4326 districts/districts.shp districts/nyedwi.shp

chunks: directories
	python chunk.py buildings/buildings.shp districts/districts.shp chunks/buildings-%s.shp ElectDist
	python chunk.py addresses/addresses.shp districts/districts.shp chunks/addresses-%s.shp ElectDist

directories:
	mkdir -p chunks
	mkdir -p osm

osm: chunks
	python convert.py
