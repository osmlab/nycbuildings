--The early import did not merge address nodes into the building.
--This script will find these buildings and generate a list of way geometries that need correction
--This script is not optimized and will literally take DAYS on a large extract! Use on a small area!

--createAreas MUST be run first!


--FINAL RESULTS - ANY BUILDING WITH 1 ADDR NODE
DROP TABLE IF EXISTS building_merge;
CREATE TABLE building_merge();
SELECT AddGeometryColumn('building_merge', 'geom', 4326, 'POLYGON', 2);

--PROCESSING - ANY BUILDING WITH ANY # of ADDR NODES
DROP TABLE IF EXISTS building_contains;
CREATE TABLE building_contains();
SELECT AddGeometryColumn('building_contains', 'geom', 4326, 'POLYGON', 2);CEDURE--
CREATE OR REPLACE VIEW node_geom AS SELECT geom FROM nodes, node_tags WHERE k='addr:housenumber' AND id = node_id; 

--FUNCTIONS--

DROP FUNCTION IF EXISTS contains();

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


SELECT contains();
