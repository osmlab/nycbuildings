// Look for buildings with both, queens and non-queens addresses
// See https://github.com/osmlab/nycbuildings/issues/35
// node 0.10.x
// Usage:
// ulimit -n 7000 # set ulimit high enough to read all files
// node validation/historicaddresses.js merged/* > historicaddresses.csv
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
        buildings.forEach(function(building) {
            var addresses = building.properties['addresses'];
            var housenumbers =
                _.chain(addresses)
                .pluck('properties')
                .reduce(function(memo, p) {
                    memo[p['STREET_NAM']] = memo[p['STREET_NAM']] || [];
                    memo[p['STREET_NAM']].push(p['HOUSE_NUMB']);
                    return memo;
                }, {});
            var mixed = false;
            _(housenumbers).each(function(numbers, street) {
                var queens = 0;
                var notQueens = 0;
                _(numbers).each(function(number) {
                    if (number.indexOf('-') == -1) {
                        notQueens++;
                    } else {
                        queens++;
                    }
                });
                if (queens > 0 && notQueens > 0) {
                    mixed = true;
                }
            });
            if (mixed) {
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
            }
        });
    });
});
