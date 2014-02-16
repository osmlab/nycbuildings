// Look for buildings with both, queens and non-queens addresses
// See https://github.com/osmlab/nycbuildings/issues/35
// node 0.10.x
// Usage:
// ulimit -n 7000 # set ulimit high enough to read all files
// node validation/historicaddresses.js merged/* > historicaddresses.csv
var fs = require('fs');

console.log('address,specialcode,lng,lat');
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
        buildings.forEach(function(building) {
            var addresses = building.properties['addresses'];
            if (addresses.length > 2) {
                var queens = 0;
                var notQueens = 0;
                addresses.forEach(function(address) {
                    if (address.properties['HOUSE_NUMB'].indexOf('-') == -1) {
                        notQueens++;
                    } else {
                        queens++;
                    }
                });
                if (queens > 0 && notQueens > 0) {
                    addresses.forEach(function(a) {
                        console.log(
                            a.properties['STREET_NAM'] + ' ' + a.properties['HOUSE_NUMB'] + ',' +
                            a.properties['SPECIAL_CO'] + ',' +
                            a.geometry.coordinates[0] + ',' +
                            a.geometry.coordinates[1]
                        );
                    });
                }
            }
        });
    });
});
