NYC building and address import
==============================

**[Work in progress, see proposal](http://wiki.openstreetmap.org/wiki/Import/Catalogue/NYC_Buildings_Addresses)**

Generates an OSM file of buildings with addresses per NYC election districts,
ready to be used in JOSM for a manual review and upload to OpenStreetMap.

## Data

- [Building perimeter outlines](https://dl.dropboxusercontent.com/u/479174/NYC/BUILDING_7_25_13.zip)
- [Address points](https://dl.dropboxusercontent.com/u/479174/NYC/NYC_AddressPoint.zip)

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
    python convert.py 65001


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
    height="HEIGHT_ROO" # If available
    addr:housenumber="HOUSE_NUMB" # If available
    addr:streetname="STREET_NAM" # If available
    addr:postcode="ZIPCODE" # If available

(All "addr" entities in CAPS are from address file.)

*Addresses*

Each address is a node tagged with:

    addr:housenumber="HOUSE_NUMB"
    addr:streetname="STREET_NAM"
    addr:postcode=ZIPCODE

(All entities in CAPS from address file.)

## Related

- [NYC possible imports](http://wiki.openstreetmap.org/wiki/New_York,_New_York#Possible_Imports)
