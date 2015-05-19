# Clean up special_co adrees(A,B) in NYC

## 
I've done a script to make URL's from all places where  there are  special-co(A,B) address.

Grid for  

- [special_co(A)](https://github.com/Rub21/clean-up-address-NYC/blob/master/grid-a-NYC.geojson)

- [special_co(B)](https://github.com/Rub21/clean-up-address-NYC/blob/master/grid-b-NYC.geojson)


## How to run

`git clone https://github.com/Rub21/clean-up-address-NYC.git`

`cd clean-up-address-NYC`

`npm install`

- `node index.js --csvfile=a.csv --geofile=grid-a-NYC.geojson`

- `node index.js --csvfile=b.csv --geofile=grid-b-NYC.geojson`

*it will be create a files called:*

- a-urls-1.csv,a-urls-2.csv ...


- b-urls-1.csv,b-urls-2.csv ...


Copy the text from each csv file and paste in a ticked. 


Click a URL in ticked.  it will be download the objects with special_co (A) and special_co(B) in JOSM.

and use the next maps in backgroud to fix the adress.

-  special_co(A)

`https://b.tiles.mapbox.com/v4/ruben.b62d31b1/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoicnViZW4iLCJhIjoiYlBrdkpRWSJ9.JgDDxJkvDn3us36aGzR6vg`

-  special_co(B)

`https://a.tiles.mapbox.com/v4/ruben.61efb1aa/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoicnViZW4iLCJhIjoiYlBrdkpRWSJ9.JgDDxJkvDn3us36aGzR6vg`



# How to work

when you download the data:

- If the osm objects are/is points as address, remove these points and upload the change or if these point  has a other tag added by users, just remove the tag `addr:housenumber` and `addr:street` 

- If the  osm objects   are ways or relation (buildings), remove  the tag `addr:housenumber` and `addr:street` and upload the change

-  If the URL does not give you any data, it is because there is not  any special_co(A,B) address in download place 
