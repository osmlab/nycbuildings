--This script will find all buildings with a single address node
--createAreas MUST be run first!

--Clear Database
DROP TABLE IF EXISTS merge_geom; --Building With 1+ nodes
DROP TABLE IF EXISTS final_geom; --Building with 1 node (Final Data)
DROP FUNCTION IF EXISTS contains();

--Create Tables
CREATE TABLE merge_geom();
CREATE TABLE final_geom();

--Add Geom Cols
SELECT AddGeometryColumn('merge_geom', 'geom', 4326, 'POLYGON', 2);
SELECT AddGeometryColumn('final_geom', 'geom', 4326, 'POLYGON', 2);

CREATE FUNCTION contains() RETURNS void AS $$
	DECLARE
		wayID RECORD;
		nodeID RECORD;
	BEGIN
		FOR wayID IN SELECT * FROM building_geom LOOP
			FOR nodeID IN SELECT * FROM addr_geom LOOP
				IF ST_Contains(wayID.geom, nodeID.geom) THEN
					RAISE NOTICE 'ADDR IN WAY: %', wayID.geom;
					INSERT INTO merge_geom(geom) VALUES (wayID.geom);
                    DELETE FROM addr_geom WHERE geom = nodeID.geom; --Node does not need to be checked after ST_Contains returns true
				END IF;
			END LOOP;
		END LOOP;
		
        --Removes Ways with 2+ nodes
		RAISE NOTICE 'DETERMINING UNIQUE RESULTS';
		INSERT INTO building_merge SELECT DISTINCT geom FROM building_contains;
		RAISE NOTICE 'PROCESSING COMPLETE';
END;
$$ LANGUAGE plpgsql;

SELECT contains();
