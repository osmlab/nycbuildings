--Find all addr:streets without 'th ', 'st ', 'rd ', or 'nd' and with a number
SELECT way_id FROM way_tags WHERE k='addr:street' AND LOWER(v) NOT SIMILAR TO '%[0-9]th %' AND LOWER(v) NOT SIMILAR TO '%[0-9]st %' AND LOWER(v) NOT SIMILAR TO '%[0-9]rd %' AND LOWER(v) NOT SIMILAR TO '%[0-9]nd' AND LOWER(v) SIMILAR TO '%[0-9] %';
