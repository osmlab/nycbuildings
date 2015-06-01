NYC building and address import
==============================

Generates an OSM file of buildings with addresses per NYC election districts,
ready to be used in JOSM for a manual review and upload to OpenStreetMap.

This README is about data conversion. Find **[Import guidelines in the Wiki](https://github.com/osmlab/nycbuildings/wiki)**.

## Blog posts

- [Importing 1 million New York City buildings and addresses](http://www.openstreetmap.org/user/lxbarth/diary/23588)
- [Over 1 million New York City buildings and addresses imported to OpenStreetMap](https://www.mapbox.com/blog/nyc-buildings-openstreetmap/)

## Data

[See documentation on OSM Wiki](http://wiki.openstreetmap.org/wiki/Import/Catalogue/NYC_Buildings_Addresses)

## Status

- Needs peer review

## Prerequisites 

    Python 2.7.x
    pip
    virtualenv
    libxml2
    libxslt
    spatialindex
    GDAL

### Installing prerequisites on Mac OSX
  
    # install brew http://brew.sh

    brew install libxml2 
    brew install libxslt 
    brew install spatialindex 
    brew install gdal 

### Installing prerequisites on Ubuntu

    apt-get install python-pip
    apt-get install python-virtualenv
    apt-get install gdal-bin
    apt-get install libgdal-dev
    apt-get install libxml2-dev
    apt-get install libxslt-dev
    apt-get install python-lxml
    apt-get install python-dev
    apt-get install libspatialindex-dev
    apt-get install unzip

## Set up Python virtualenv and get dependencies
    # may need to easy_install pip and pip install virtualenv 
    virtualenv ~/venvs/nycbuildings
    source ~/venvs/nycbuildings/bin/activate 
    pip install -r requirements.txt


## Usage

Run all stages:

    # Download all files and process them into a building
    # and an address .osm file per district.
    make

You can run stages separately, like so:

    # Download and expand all files, reproject
    make download

    # Chunk address and building files by district
    make chunks

    # Generate importable .osm files.
    # This will populate the osm/ directory with one .osm file per
    # NYC election district.
    make osm

    # Clean up all intermediary files:
    make clean

    # For testing it's useful to convert just a single district.
    # For instance, convert election district 65001:
    make merged # Will take a while
    python convert.py merged/buildings-addresses-65001.geojson # Fast


## Features

- Conflates buildings and addresses
- Cleans address names
- Exports one OSM XML building file per NYC election district
- Exports OSM XML address files for addresses that pertain to buildings with
  more than one address
- Handles multipolygons
- Simplifies building shapes

## Attribute mapping

*Buildings*

Each building is a closed way tagged with:

    building="yes"
    height="HEIGHT_ROO" # In meters, if available
    addr:housenumber="HOUSE_NUMB" # If available
    addr:streetname="STREET_NAM" # If available
    addr:postcode="ZIPCODE" # If available
    nycdoitt:bin="BIN" # NYC DoITT building identifier

(All "addr" entities in CAPS are from address file.)

*Addresses*

Each address is a node tagged with:

    addr:housenumber="HOUSE_NUMB"
    addr:streetname="STREET_NAM"
    addr:postcode="ZIPCODE"

(All entities in CAPS from address file.)

### House number attributes

House number attributes are captured in 5 columns of the address shape file.

There are four fields that begin with `HOUSE_NU` and one named `HYPHEN_TYPE`.

    HOUSE_NUMBER (HOUSE_NUMB):
    Alias: HOUSE_NUMBER
    Data type: String
    Width: 9
    Precision: 0
    Scale: 0

Definition: Stores the address number.  The field will support hyphenated and range based addresses. Excludes suffixes.

    HOUSE_NUMBER_SUFFIX (HOUSE_NU_1):
    Alias: HOUSE_NUMBER_SUFFIX
    Data type: String
    Width: 9
    Precision: 0
    Scale: 0

Definition: It contains any suffix (e.g. 1/2, A, B) associated with the house number.  GARAGE and REAR are not captured.

    HOUSE_NUMBER_RANGE (HOUSE_NU_2):
    Alias: HOUSE_NUMBER_RANGE
    Data type: String
    Width: 9
    Precision: 0
    Scale: 0

Definition: Stores the minimum and maximum numbers of a range assigned to a building. Unlike a hyphen these are separate building numbers found on a building. Co-op City is an example.

    HOUSE_NUMBER_RANGE_SUFFIX (HOUSE_NU_3):
    Alias: HOUSE_NUMBER_RANGE_SUFFIX
    Data type: String
    Width: 9
    Precision: 0
    Scale: 0

Definition: Stores suffixes associated with `HOUSE_NUMBER_RANGE` addresses.

    HYPHEN_TYPE
    Alias: HYPHEN_TYPE
    Data type: String
    Width: 1
    Precision: 0
    Scale: 0

Definition: The Address Point Feature Class will support the storage of hyphenated addresses.  There are three domain values associated with hyphen types: 1) Building Ranges, 2) "Queens" style hyphens and 3) Floor numbers.

## Related

- [NYC possible imports](http://wiki.openstreetmap.org/wiki/New_York,_New_York#Possible_Imports)
