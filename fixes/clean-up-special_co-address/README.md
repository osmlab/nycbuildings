# Clean up special_co adrees(A,B) in NYC

## 
I've done a script to make URL's from all places where  there are  special-co(A,B) address.

Grid for  

- [special_co(A)](https://github.com/osmlab/nycbuildings/tree/master/fixes/clean-up-special_co-address/blob/master/grid-a-NYC.geojson)

- [special_co(B)](https://github.com/osmlab/nycbuildings/tree/master/fixes/clean-up-special_co-address/blob/master/grid-b-NYC.geojson)


## How to run

`git clone https://github.com/osmlab/nycbuildings.git`

`cd nycbuildings/fixes/clean-up-special_co-address/`

`npm install`

- `node index.js --csvfile=a.csv --geofile=grid-a-NYC.geojson`

- `node index.js --csvfile=b.csv --geofile=grid-b-NYC.geojson`

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

`https://b.tiles.mapbox.com/v4/ruben.b62d31b1/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoicnViZW4iLCJhIjoiYlBrdkpRWSJ9.JgDDxJkvDn3us36aGzR6vg`

-  special_co(B)

`https://a.tiles.mapbox.com/v4/ruben.61efb1aa/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoicnViZW4iLCJhIjoiYlBrdkpRWSJ9.JgDDxJkvDn3us36aGzR6vg`



# How to work

https://github.com/osmlab/nycbuildings/wiki/Import-cleanup