// Look for special addresses
// See https://github.com/osmlab/nycbuildings/issues/35#issuecomment-34885728
// node 0.10.x
// Usage:
// ulimit -n 7000 # set ulimit high enough to read all files
// node validation/specialaddresses.js merged/* > specialaddresses.csv
var fs = require('fs');
var _ = require('underscore');

console.log('address,perbuilding,specialcode,lng,lat');
process.argv.splice(2).forEach(function(file) {
    fs.readFile(file, function(err, data) {
        if (err) {
            console.error(file);
            console.error(err);
            return;
        }
        try {
            var buildings = JSON.parse(data);
        }
        catch (err) {
            console.error(file);
            console.error(err);
            return;
        }        
        var coordinates = [];
        buildings.forEach(logSpecial);
    });
});

var logSpecial = function(building) {
    var addresses = building.properties['addresses'];
    if (_.chain(addresses).pluck('properties').pluck('SPECIAL_CO').without(null, 'null').value().length == 0) {
        return;
    }
    addresses.forEach(function(a) {
        var housenumber = a.properties['HOUSE_NUMB'];
        if (a.properties['HOUSE_NU_1']) {
            housenumber += ' ' + a.properties['HOUSE_NU_1'];
        }
        console.log(
            housenumber + ' ' + a.properties['STREET_NAM'] + ',' + 
            addresses.length + ',' + 
            a.properties['SPECIAL_CO'] + ',' + 
            a.geometry.coordinates[0] + ',' + 
            a.geometry.coordinates[1]
        );
    });
};
