var fs = require('fs');
var _ = require('underscore');
var argv = require('optimist').argv;
var csv = require('csv-parser');
var spreadsheets = [];
var grid = JSON.parse(fs.readFileSync(argv.geofile, 'utf8'));
_.each(grid.features, function(val) {
	get_url(val);
});

function get_url(val) {
	var urls = [];
	var url = 'http://127.0.0.1:8111/import?url=http://overpass.osm.rambler.ru/cgi/interpreter?data=[out:xml][timeout:50];(';
	var counter = 0;
	var rqt = fs.createReadStream(argv.csvfile)
		.pipe(csv())
		.on('data', function(data) {
			var point = [parseFloat(data.x), parseFloat(data.y)];
			if (pointinpolygon(point, val.geometry.coordinates[0])) {
				counter++;
				var thenum = data.streetname.replace(/[^0-9]/g, '');
				if (thenum !== '') {
					data.streetname = data.streetname.replace(thenum, getGetOrdinal(thenum));
				}
				var bbox = [val.properties.top, val.properties.left, val.properties.bottom, val.properties.right];
				var node = 'node["addr:housenumber"="' + data.house_num + '"]["addr:street"="' + data.streetname.toLowerCase().capitalize() + '"](' + bbox.toString() + ');';
				var way = 'way["addr:housenumber"="' + data.house_num + '"]["addr:street"="' + data.streetname.toLowerCase().capitalize() + '"](' + bbox.toString() + ');';
				var relation = 'relation["addr:housenumber"="' + data.house_num + '"]["addr:street"="' + data.streetname.toLowerCase().capitalize() + '"](' + bbox.toString() + ');';
				url += node + way + relation;
				if (counter === 20) {
					url += ');out meta;>;out meta qt;';
					urls.push(url);
					url = 'http://127.0.0.1:8111/import?url=http://overpass.osm.rambler.ru/cgi/interpreter?data=[out:xml][timeout:50];(';
					counter = 0;
				}
			}
		});

	rqt.on('finish', function() {
		url += ');out meta;>;out meta qt;';
		urls.push(url);
		for (var i = 0; i < urls.length; i++) {
			if (urls[i].length > 133) {
				var text = '- [ ] [' + val.properties.id + '-' + (i + 1) + '](' + urls[i] + ') \n';
				if (val.properties.id <= 100) fs.appendFile(argv.csvfile.split('.')[0] + "-urls-1.csv", text, function(err) {});
				if (val.properties.id > 100 && val.properties.id <= 200) fs.appendFile(argv.csvfile.split('.')[0] + "-urls-2.csv", text, function(err) {});
				if (val.properties.id > 200 && val.properties.id <= 300) fs.appendFile(argv.csvfile.split('.')[0] + "-urls-3.csv", text, function(err) {});
				if (val.properties.id > 300 && val.properties.id <= 400) fs.appendFile(argv.csvfile.split('.')[0] + "-urls-4.csv", text, function(err) {});
				if (val.properties.id > 400) fs.appendFile(argv.csvfile.split('.')[0] + "-urls-5.csv", text, function(err) {});
			}
		};
	});
}

function getGetOrdinal(n) {
	var s = ["th", "st", "nd", "rd"],
		v = n % 100;
	return n + (s[(v - 20) % 10] || s[v] || s[0]);
}

function pointinpolygon(point, vs) {
	var x = point[0],
		y = point[1];
	var inside = false;
	for (var i = 0, j = vs.length - 1; i < vs.length; j = i++) {
		var xi = vs[i][0],
			yi = vs[i][1];
		var xj = vs[j][0],
			yj = vs[j][1];
		var intersect = ((yi > y) != (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
		if (intersect) inside = !inside;
	}
	return inside;
}

String.prototype.capitalize = function() {
	return this.replace(/(^|\s)([a-z])/g, function(m, p1, p2) {
		return p1 + p2.toUpperCase();
	});
};