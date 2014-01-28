--The early import did not merge address nodes into the building.
--This script will find these buildings and generate a list of way geometries that need correction
--This script is not optimized and will literally take DAYS on a large extract! Use on a small area!

--PROCEDURE--
CREATE OR REPLACE VIEW node_geom AS SELECT geom FROM nodes, node_tags WHERE k='addr:housenumber' AND id = node_id; 

--PROCESSING - ANY BUILDING WITH ANY # of ADDR NODES
DROP TABLE IF EXISTS building_contains;
CREATE TABLE building_contains();
SELECT AddGeometryColumn('building_contains', 'geom', 4326, 'POLYGON', 2);

--FINAL RESULTS - ANY BUILDING WITH 1 ADDR NODE
DROP TABLE IF EXISTS building_merge;
CREATE TABLE building_merge();
SELECT AddGeometryColumn('building_merge', 'geom', 4326, 'POLYGON', 2);

DROP TABLE IF EXISTS way_geom;
CREATE TABLE way_geom();
SELECT AddGeometryColumn('way_geom', 'geom', 4326, 'POLYGON', 2);

--FUNCTIONS--
DROP FUNCTION IF EXISTS wayToGeom();
DROP FUNCTION IF EXISTS contains();

CREATE FUNCTION wayToGeom() RETURNS void AS $$
	DECLARE
		way_row RECORD;
		wayID bigint;
	BEGIN
		FOR way_row IN SELECT * FROM way_tags WHERE k='building' ORDER BY way_id LOOP
			wayID := way_row.way_id;
			
			INSERT INTO way_geom (geom) SELECT ST_MakePolygon(ST_MakeLine(geom ORDER BY sequence_id)) FROM (SELECT geom, sequence_id FROM nodes, way_nodes WHERE way_id = wayID AND node_id = id) way;
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

CREATE FUNCTION contains() RETURNS void AS $$
	DECLARE
		wayID RECORD;
		nodeID RECORD;
	BEGIN
		FOR wayID IN SELECT * FROM way_geom LOOP
			RAISE NOTICE 'Testing Way: %', wayID.geom;
			FOR nodeID IN SELECT * FROM node_geom LOOP
				IF ST_Contains(wayID.geom, nodeID.geom) THEN
					RAISE NOTICE 'NODE IN BUILDING';
					INSERT INTO building_contains(geom) VALUES (wayID.geom);
				END IF;
			END LOOP;
		END LOOP;
		
		--Removes Buildings that contain multiple nodes
		RAISE NOTICE 'REMOVING DUPS';
		INSERT INTO building_merge SELECT DISTINCT geom FROM building_contains;
		RAISE NOTICE 'PROCESSING COMPLETE';
END;
$$ LANGUAGE plpgsql;

SELECT wayToGeom();
SELECT contains();
