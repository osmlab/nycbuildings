--Buildings should be tagged `building=school` instead of `amenity=school`
--This file will generate a list of buildings that need to be manually fixed by
--Removing the amenity and name tag and putting them on a polygon around the school yard.

CREATE OR REPLACE VIEW buildings AS SELECT way_id FROM way_tags WHERE k='building';

DROP TABLE IF EXISTS school_errors;
CREATE TABLE school_errors(id bigint NOT NULL);

INSERT INTO school_errors SELECT buildings.way_id FROM buildings, way_tags WHERE k='amenity' AND 
v='school' AND buildings.way_id = way_tags.way_id;

DROP VIEW buildings;
