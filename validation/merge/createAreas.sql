--Convert to PostGIS GEOM types for easier management 

--Clear Database
DROP TABLE IF EXISTS addr_geom;
DROP TABLE IF EXISTS building_geom;
DROP FUNCTION IF EXISTS wayToGeom();
DROP TABLE IF EXISTS buildings_tmp;
DROP TABLE IF EXISTS addrway_tmp;
DROP TABLE IF EXISTS addrway_final_tmp;

--Create Tables
CREATE TABLE addr_geom();
CREATE TABLE building_geom(way_id bigint);

--Temp Tables
CREATE TABLE buildings_tmp(way_id bigint);
CREATE TABLE addrway_tmp(way_id bigint);
CREATE TABLE addrway_final_tmp(way_id bigint);

--Add Geometry Cols
SELECT AddGeometryColumn('building_geom', 'geom', 4326, 'POLYGON', 2);
SELECT AddGeometryColumn('addr_geom', 'geom', 4326, 'POINT', 2);

--Populate addr_geom
INSERT INTO addr_geom SELECT geom FROM nodes, node_tags WHERE k='addr:housenumber' AND id = node_id;

--Populate buildings_tmp & addrway_tmp
INSERT INTO buildings_tmp SELECT way_id FROM way_tags WHERE k='building';
INSERT INTO addrway_tmp SELECT buildings_tmp.way_id FROM buildings_tmp, way_tags WHERE buildings_tmp.way_id = way_tags.way_id AND k NOT iLIKE 'addr%';
INSERT INTO addrway_final_tmp SELECT DISTINCT way_id FROM addrway_tmp;

--Populate building_geom
CREATE FUNCTION wayToGeom() RETURNS void AS $$
	DECLARE
		way_row RECORD;
		wayID bigint;
	BEGIN
		FOR way_row IN SELECT * FROM way_tags WHERE k='building' ORDER BY way_id LOOP
			wayID := way_row.way_id;
			
			INSERT INTO building_geom (way_id, geom) SELECT wayID, ST_MakePolygon(ST_MakeLine(geom ORDER BY sequence_id)) FROM (SELECT geom, sequence_id FROM nodes, way_nodes WHERE way_id = wayID AND node_id = id) way;
		END LOOP;
	EXCEPTION
		WHEN others THEN
            --This usually occurs when a line is tagged as a building
            --Or when osmosis has broken a building when the file is split.
            --The program must be started over if this error occurs
            RAISE NOTICE 'ERROR ON: % REMOVING WAY', wayID;
            DELETE FROM way_tags WHERE way_id = wayID;
            DELETE FROM ways WHERE id = wayID;
            DELETE FROM way_nodes WHERE way_id = wayID;
END;
$$ LANGUAGE plpgsql;

SELECT wayToGeom();

--Remove temporary tables
--DROP TABLE buildings_tmp;
--DROP TABLE addrway_tmp;
