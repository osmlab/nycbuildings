all: BldgPly/buildings.shp DistPly/districts.shp directories chunks osm

clean:
	rm -f BldgPly.zip
	rm -f DistPly.zip

BldgPly.zip:
	curl -L "https://nycopendata.socrata.com/api/geospatial/r7fd-yd5e?method=export&format=Shapefile" -o BldgPly.zip

DistPly.zip:
	curl -L "http://www.nyc.gov/html/dcp/download/bytes/nyedwi_13a.zip" -o DistPly.zip

BldgPly: BldgPly.zip
	unzip BldgPly.zip -d BldgPly

DistPly: DistPly.zip
	unzip DistPly.zip -d DistPly

BldgPly/buildings.shp: BldgPly
	rm -f BldgPly/buildings.*
	ogr2ogr -simplify 0.2 -t_srs EPSG:4326 -overwrite BldgPly/buildings.shp BldgPly/DOITT_BUILDING_01_13SEPT2010.shp

DistPly/districts.shp: DistPly
	rm -f DistPly/districts.*
	ogr2ogr -t_srs EPSG:4326 DistPly/districts.shp DistPly/nyedwi.shp

chunks: directories
	python chunk.py BldgPly/buildings.shp DistPly/districts.shp chunks/buildings-%s.shp ElectDist

osm: directories
	python convert.py

directories:
	mkdir -p chunks
	mkdir -p osm
