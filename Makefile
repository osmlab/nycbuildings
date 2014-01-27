all: buildings/buildings.shp addresses/addresses.shp districts/districts.shp chunks osm

download: districts/districts.shp addresses/addresses.shp buildings/buildings.shp

clean:
	rm -f building_footprints_shape_09-13.zip
	rm -f NYC_AddressPoint.zip
	rm -f nyedwi_13a.zip

building_footprints_shape_09-13.zip:
	curl -L "https://data.cityofnewyork.us/download/tb92-6tj8/application/zip" -o building_footprints_shape_09-13.zip

NYC_AddressPoint.zip:
	curl -L "https://dl.dropboxusercontent.com/u/479174/NYC/NYC_AddressPoint.zip" -o NYC_AddressPoint.zip

nyedwi_13a.zip:
	curl -L "http://www.nyc.gov/html/dcp/download/bytes/nyedwi_13a.zip" -o nyedwi_13a.zip

buildings: building_footprints_shape_09-13.zip
	rm -rf buildings
	unzip building_footprints_shape_09-13.zip -d buildings
	rm -rf building_footprints_shape_09-13.zip

addresses: NYC_AddressPoint.zip
	rm -rf addresses
	unzip NYC_AddressPoint.zip -d addresses
	rm NYC_AddressPoint.zip

districts: nyedwi_13a.zip
	rm -rf districts
	unzip -d districts -j nyedwi_13a.zip
	rm nyedwi_13a.zip

buildings/buildings.shp: buildings
	rm -f buildings/buildings.*
	ogr2ogr -simplify 0.2 -t_srs EPSG:4326 -overwrite buildings/buildings.shp buildings/building_0913.shp

addresses/addresses.shp: addresses
	rm -f addresses/addresses.*
	ogr2ogr -t_srs EPSG:4326 -overwrite addresses/addresses.shp addresses/NYC_AddressPoint.shp

districts/districts.shp: districts
	rm -f districts/districts.*
	ogr2ogr -simplify 20 -t_srs EPSG:4326 -overwrite districts/districts.shp districts/nyedwi.shp

chunks: directories addresses/addresses.shp buildings/buildings.shp districts/districts.shp
	python chunk.py buildings/buildings.shp districts/districts.shp chunks/buildings-%s.shp ElectDist
	python chunk.py addresses/addresses.shp districts/districts.shp chunks/addresses-%s.shp ElectDist

directories:
	mkdir -p chunks
	mkdir -p osm

osm: chunks
	python convert.py
