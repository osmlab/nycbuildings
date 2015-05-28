var fs = require('fs');
var csv = require('csv-parser')
var _ = require('underscore');
var argv = require('optimist').argv;

fs.writeFile(argv.file.split('.')[0] + "-processed.csv", "shapeid,x,y,address\n", function(err) {});
var rqt = fs.createReadStream(argv.file)
	.pipe(csv())
	.on('data', function(data) {

		var thenum = data.streetname.replace(/[^0-9]/g, '');
		if (thenum !== '') {
			data.streetname = data.streetname.replace(thenum, getGetOrdinal(thenum));
		}
		var n = fix_num(data.house_num);
		console.log(data.house_num + '->' + n);
		var d = data.shapeid + "," + data.x + "," + data.y + "," + fix_num(data.house_num) + " " + data.streetname.toLowerCase().capitalize() + "\n";
		fs.appendFile(argv.file.split('.')[0] + "-processed.csv", d, function(err) {});

	});

function getGetOrdinal(n) {
	var s = ["th", "st", "nd", "rd"],
		v = n % 100;
	return n + (s[(v - 20) % 10] || s[v] || s[0]);
}

function fix_num(n) {
	if (n.indexOf('-') > 0) {
		var arr = n.split('-');
		var num_house = "";
		for (var i = 0; i < arr.length; i++) {
			var dig = arr[i].replace(/^0+/, '');
			if (_.isNumber(arr[i])) {
				if (i === 0) {
					num_house += parseInt(dig);
				} else {
					num_house += '-' + parseInt(dig);
				}
			} else {
				if (i === 0) {
					num_house += dig;
				} else {
					num_house += '-' + dig;
				}
			}
		};
		return num_house.toString();
	} else if (_.isNumber(n)) {
		return parseInt(n).toString();
	} else {
		return n.toString();
	}
}

String.prototype.capitalize = function() {
	return this.replace(/(^|\s)([a-z])/g, function(m, p1, p2) {
		return p1 + p2.toUpperCase();
	});
};