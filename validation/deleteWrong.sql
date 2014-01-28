--The merge script cannot handle lines that have been tagged with building=* as it cannot
--convert the line into a postgis polygon geometry. Replace the delid with the script with the
--problematic way and this will remove it from the local database.

CREATE OR REPLACE FUNCTION remove() RETURNS void AS $$
DECLARE
    delid bigint := 157892200;
BEGIN
	RAISE NOTICE 'REMOVING %', delid;
	DELETE FROM way_tags WHERE way_id = delid;
	DELETE FROM ways WHERE id = delid;
	DELETE FROM way_nodes WHERE way_id = delid;
END;
$$ LANGUAGE plpgsql;

SELECT remove();
