# Creates an addresses/addresses_formatted.shp
# with the house number part of the address formatted.
# Used for prototyping, not for the actual conversion.

from shapely.geometry import mapping
import fiona
from pprint import pprint

# HOUSE_NUMB ... house number
# HOUSE_NU_1 ... house number suffix
# HOUSE_NU_2 ... house number range
# HOUSE_NU_3 ... house number range suffix
# HYPHEN_TYP ... hyphen type
#    Q ... Queens type
#    R ... range
#    X ... Queens type range (effectively same as R)
#    N ... none
def format_housenumber(p):
    def suffix(part1, part2, hyphen_type=None):
        if not part2:
            return part1
        if hyphen_type == 'U': # unit numbers
            return part1 + '-' + part2
        if len(part2) == 1 and part2.isalpha(): # single letter extensions
            return part1 + part2
        return part1 + ' ' + part2 # All others
    number = suffix(p['HOUSE_NUMB'], p['HOUSE_NU_1'], p['HYPHEN_TYP'])
    if p['HOUSE_NU_2']:
        number = number + ' - ' + suffix(p['HOUSE_NU_2'], p['HOUSE_NU_3'])
    return number

# open the polygon shapefile
with fiona.collection('addresses/addresses.shp', 'r') as addresses:
    # copy of the schema of the original polygon shapefile to the output shapefile (copy)
    schema = addresses.schema.copy()
    # creation of the new field color in the new schema
    schema['properties']['FORMATTED'] = 'str' 
    # output shapefile with the new schema
    with fiona.collection('addresses/addresses_formatted.shp', 'w', 'ESRI Shapefile', schema) as output:
        # construction of the new shapefile
        records = []
        for address in addresses:
            address['properties']['FORMATTED'] = format_housenumber(address['properties'])
            records.append(address)
        output.writerecords(records)
