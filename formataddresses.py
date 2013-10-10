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
    number = p['HOUSE_NUMB']
    if p['HOUSE_NU_1']:
        if p['HYPHEN_TYP'] == 'U': # this case only exists for HOUSE_NU_1, not HOUSE_NU_3
            number = number + '-' + p['HOUSE_NU_1']
        else:
            number = number + ' ' + p['HOUSE_NU_1']
    number_range = p['HOUSE_NU_2']
    if p['HOUSE_NU_3']:
        number_range = number_range + p['HOUSE_NU_3']
    if number_range:
        number = number + ' - ' + number_range
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
