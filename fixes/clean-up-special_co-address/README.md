# Clean up special_co adrees(A,B) in NYC

## 
I've done a script to make URL's from all places where  there are  special-co(A,B) address.

Original files get from : https://data.cityofnewyork.us/Housing-Development/Building-Footprints/tb92-6tj8

Extract using Qgis:

- [Special-co-A](https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/a.csv)
- [Special-co-B](https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/b.csv)

Grid for both files using Qgis:

- [grid-b.geojson](https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/grid-a.geojson)

- [grid-b.geojson](https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/grid-b.geojson)


## How to run

`git clone https://github.com/osmlab/nycbuildings.git`

`cd nycbuildings/fixes/clean-up-special_co-address/`

`npm install`

*Join : "house_num" + "streetname" -> "address"*

`node fix.js --file=a.csv`

`node fix.js --file=b.csv`

*Result:*

- [a-processed.csv](https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/a-processed.csv)

- [b-processed.csv](https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/b-processed.csv)

*Get URL fron each each grid to download in JOSM*

- `node index.js --geofile=grid-a.geojson`

- `node index.js --geofile=grid-b.geojson`

*it will be create a files:*

- https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/a-urls-1.md
- https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/a-urls-2.md
- https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/a-urls-3.md
- https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/a-urls-4.md
- https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/b-urls-1.md
- https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/b-urls-2.md
- https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/b-urls-3.md
- https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/b-urls-4.md
- https://github.com/osmlab/nycbuildings/blob/master/fixes/clean-up-special_co-address/b-urls-5.md



Copy the text from each file and paste in a ticked. 


Click a URL in ticked.  it will be download the objects with special_co (A) and special_co(B) in JOSM.

and use the next maps in backgroud to fix the adress.

-  special_co(A)

`https://{switch:a,b,c}.tiles.mapbox.com/v4/ruben.ma4ko888/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoicnViZW4iLCJhIjoiYlBrdkpRWSJ9.JgDDxJkvDn3us36aGzR6vg`

-  special_co(B)

`https://{switch:a,b,c}.tiles.mapbox.com/v4/ruben.ma4lak4o/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoicnViZW4iLCJhIjoiYlBrdkpRWSJ9.JgDDxJkvDn3us36aGzR6vg`



# How to work

https://github.com/osmlab/nycbuildings/wiki/Import-cleanup