--Convert to PostGIS GEOM types for easier management 

--Clear Database
DROP TABLE IF EXISTS addr_geom;
DROP TABLE IF EXISTS building_geom;
DROP FUNCTION IF EXISTS wayToGeom();

--Create Tables
CREATE TABLE addr_geom();
CREATE TABLE building_geom();

--Add Geometry Cols
SELECT AddGeometryColumn('building_geom', 'geom', 4326, 'POLYGON', 2);
SELECT AddGeometryColumn('addr_geom', 'geom', 4326, 'POINT', 2);

--Populate addr_geom
INSERT INTO addr_geom SELECT geom FROM nodes, node_tags WHERE k='addr:housenumber' AND id = node_id;

--Populate building_geom
CREATE FUNCTION wayToGeom() RETURNS void AS $$
	DECLARE
		way_row RECORD;
		wayID bigint;
	BEGIN
		FOR way_row IN SELECT * FROM way_tags WHERE k='building' ORDER BY way_id LOOP
			wayID := way_row.way_id;
			
			INSERT INTO building_geom (geom) SELECT ST_MakePolygon(ST_MakeLine(geom ORDER BY sequence_id)) FROM (SELECT geom, sequence_id FROM nodes, way_nodes WHERE way_id = wayID AND node_id = id) way;
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
