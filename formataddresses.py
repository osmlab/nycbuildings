# Creates an addresses/addresses_formatted.shp
# with the house number part of the address formatted.
# Used for prototyping, not for the actual conversion.

from shapely.geometry import mapping
import fiona
from pprint import pprint
import re

## Formats multi part house numbers
def formatHousenumber(p):
    def suffix(part1, part2, hyphen_type=None):
        part1 = stripZeroes(part1)
        if not part2:
            return str(part1)
        part2 = stripZeroes(part2)
        if hyphen_type == 'U': # unit numbers
            return part1 + '-' + part2
        if len(part2) == 1 and part2.isalpha(): # single letter extensions
            return part1 + part2
        return part1 + ' ' + part2 # All others
    def stripZeroes(addr): # strip leading zeroes from numbers
        if addr.isdigit():
            addr = str(int(addr))
        if '-' in addr:
            try:
                addr = str(int(addr.split('-')[0])) + '-' + str(int(addr.split('-')[1]))
            except:
                pass
        return addr
    number = suffix(p['HOUSE_NUMB'], p['HOUSE_NU_1'], p['HYPHEN_TYP'])
    if p['HOUSE_NU_2']:
        number = number + ' - ' + suffix(p['HOUSE_NU_2'], p['HOUSE_NU_3'])
    return number

# Converts an address
def convertAddress(address):
    result = dict()
    if all (k in address for k in ('HOUSE_NUMB', 'STREET_NAM')):
        if address['HOUSE_NUMB']:
            result['addr:housenumber'] = formatHousenumber(address)
        if address['STREET_NAM']:
            streetname = address['STREET_NAM'].title()
            original = streetname
            streetname = re.sub(r"(.*)(\d*11)\s+(.*)", r"\1\2th \3", streetname)
            streetname = re.sub(r"(.*)(\d*12)\s+(.*)", r"\1\2th \3", streetname)
            streetname = re.sub(r"(.*)(\d*13)\s+(.*)", r"\1\2th \3", streetname)
            streetname = re.sub(r"(.*)(\d*1)\s+(.*)", r"\1\2st \3", streetname)
            streetname = re.sub(r"(.*)(\d*2)\s+(.*)", r"\1\2nd \3", streetname)
            streetname = re.sub(r"(.*)(\d*3)\s+(.*)", r"\1\2rd \3", streetname)
            streetname = re.sub(r"(.*)(\d+)\s+(.*)", r"\1\2th \3", streetname)
            if original != streetname:
                print original + "," + streetname
            result['addr:street'] = streetname
        if address['ZIPCODE']:
            result['addr:postcode'] = str(int(address['ZIPCODE']))
    return result

# open the polygon shapefile
with fiona.collection('addresses/addresses.shp', 'r') as addresses:
    print 'original,converted'
    for address in addresses:
        convertAddress(address['properties'])
