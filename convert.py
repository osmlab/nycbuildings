# Convert NYC building footprints and addresses into importable OSM files.

# profiling
import cProfile
import pstats

from lxml import etree
from lxml.etree import tostring
from shapely.geometry import Point, LineString
from sys import argv
from glob import glob
from merge import merge
import re
from decimal import Decimal, getcontext

# profiling
prW = cProfile.Profile()
prW.enable()

# Converts given buildings into corresponding OSM XML files.
def convert(buildings, osmOut):
    buildingIdx = buildings['index']
    buildings = buildings['buildings']

    # Generates a new osm id.
    osmIds = dict(node = -1, way = -1, rel = -1)
    def newOsmId(type):
        osmIds[type] = osmIds[type] - 1
        return osmIds[type]

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
                # Expand Service Road
                # See https://github.com/osmlab/nycbuildings/issues/30
                streetname = re.sub(r"(.*)\bSr\b(.*)", r"\1Service Road\2", streetname)
                # Expand cardinal directions on Service Roads
                streetname = re.sub(r"(.*\bService Road\s)\bN\b(.*)", r"\1North\2", streetname)
                streetname = re.sub(r"(.*\bService Road\s)\bE\b(.*)", r"\1East\2", streetname)
                streetname = re.sub(r"(.*\bService Road\s)\bS\b(.*)", r"\1South\2", streetname)
                streetname = re.sub(r"(.*\bService Road\s)\bW\b(.*)", r"\1West\2", streetname)
                # Expand Expressway on Service Roads
                streetname = re.sub(r"(.*)Expwy\s\bN\b(.*)", r"\1Expressway North\2", streetname)
                streetname = re.sub(r"(.*)Expwy\s\bE\b(.*)", r"\1Expressway East\2", streetname)
                streetname = re.sub(r"(.*)Expwy\s\bS\b(.*)", r"\1Expressway South\2", streetname)
                streetname = re.sub(r"(.*)Expwy\s\bW\b(.*)", r"\1Expressway West\2", streetname)
                streetname = re.sub(r"(.*)Expwy(.*)", r"\1Expressway\2", streetname)
                # Add ordinal suffixes to numerals
                streetname = re.sub(r"(.*)(\d*11)\s+(.*)", r"\1\2th \3", streetname)
                streetname = re.sub(r"(.*)(\d*12)\s+(.*)", r"\1\2th \3", streetname)
                streetname = re.sub(r"(.*)(\d*13)\s+(.*)", r"\1\2th \3", streetname)
                streetname = re.sub(r"(.*)(\d*1)\s+(.*)", r"\1\2st \3", streetname)
                streetname = re.sub(r"(.*)(\d*2)\s+(.*)", r"\1\2nd \3", streetname)
                streetname = re.sub(r"(.*)(\d*3)\s+(.*)", r"\1\2rd \3", streetname)
                streetname = re.sub(r"(.*)(\d+)\s+(.*)", r"\1\2th \3", streetname)
                result['addr:street'] = streetname
            if address['ZIPCODE']:
                result['addr:postcode'] = str(int(address['ZIPCODE']))
        return result

    # Appends new node or returns existing if exists.
    nodes = {}
    def appendNewNode(coords, osmXml):
        rlon = int(float(coords[0]*10**7))
        rlat = int(float(coords[1]*10**7))
        if (rlon, rlat) in nodes:
            return nodes[(rlon, rlat)]
        node = etree.Element('node', visible = 'true', id = str(newOsmId('node')))
        node.set('lon', str(Decimal(coords[0])*Decimal(1)))
        node.set('lat', str(Decimal(coords[1])*Decimal(1)))
        nodes[(rlon, rlat)] = node
        osmXml.append(node)
        return node

    def appendNewWay(coords, intersects, osmXml):
        way = etree.Element('way', visible='true', id=str(newOsmId('way')))
        firstNid = 0
        for i, coord in enumerate(coords):
            if i == 0: continue # the first and last coordinate are the same
            node = appendNewNode(coord, osmXml)
            if i == 1: firstNid = node.get('id')
            way.append(etree.Element('nd', ref=node.get('id')))
            
            # Check each way segment for intersecting nodes
            int_nodes = {}
            try:
                line = LineString([coord, coords[i+1]])
            except IndexError:
                line = LineString([coord, coords[1]])
            for idx, c in enumerate(intersects):
                if line.buffer(0.000001).contains(Point(c[0], c[1])) and c not in coords:
                    t_node = appendNewNode(c, osmXml)
                    for n in way.iter('nd'):
                        if n.get('ref') == t_node.get('id'):
                            break
                    else:
                        int_nodes[t_node.get('id')] = Point(c).distance(Point(coord))
            for n in sorted(int_nodes, key=lambda key: int_nodes[key]): # add intersecting nodes in order
                way.append(etree.Element('nd', ref=n))
            
        way.append(etree.Element('nd', ref=firstNid)) # close way
        osmXml.append(way)
        return way

    # Appends an address to a given node or way.
    def appendAddress(address, element):
        for k, v in convertAddress(address['properties']).iteritems():
            element.append(etree.Element('tag', k=k, v=v))

    # Appends a building to a given OSM xml document.
    def appendBuilding(building, address, osmXml):
        # Check for intersecting buildings
        intersects = []
        for i in buildingIdx.intersection(building['shape'].bounds):
            try:
                for c in buildings[i]['shape'].exterior.coords:
                    if Point(c[0], c[1]).buffer(0.000001).intersects(building['shape']):
                        intersects.append(c)
            except AttributeError:
                for c in buildings[i]['shape'][0].exterior.coords:
                    if Point(c[0], c[1]).buffer(0.000001).intersects(building['shape']):
                        intersects.append(c)
        
        # Export building, create multipolygon if there are interior shapes.
        interiors = []
        try:
            way = appendNewWay(list(building['shape'].exterior.coords), intersects, osmXml)
            for interior in building['shape'].interiors:
                interiors.append(appendNewWay(list(interior.coords), [], osmXml))
        except AttributeError:
            way = appendNewWay(list(building['shape'][0].exterior.coords), intersects, osmXml)
            for interior in building['shape'][0].interiors:
                interiors.append(appendNewWay(list(interior.coords), [], osmXml))
        if len(interiors) > 0:
            relation = etree.Element('relation', visible='true', id=str(newOsmId('way')))
            relation.append(etree.Element('member', type='way', role='outer', ref=way.get('id')))
            for interior in interiors:
                relation.append(etree.Element('member', type='way', role='inner', ref=interior.get('id')))
            relation.append(etree.Element('tag', k='type', v='multipolygon'))
            osmXml.append(relation)
            way = relation
        way.append(etree.Element('tag', k='building', v='yes'))
        if 'HEIGHT_ROO' in building['properties']:
            height = round(((building['properties']['HEIGHT_ROO'] * 12) * 0.0254), 1)
            if height > 0:
                way.append(etree.Element('tag', k='height', v=str(height)))
        if 'BIN' in building['properties']:
            way.append(etree.Element('tag', k='nycdoitt:bin', v=str(building['properties']['BIN'])))
        if address: appendAddress(address, way)

    # Export buildings & addresses. Only export address with building if there is exactly
    # one address per building. Export remaining addresses as individual nodes.
    addresses = []
    osmXml = etree.Element('osm', version='0.6', generator='alex@mapbox.com')
    for building in buildings:
        address = None
        if len(building['properties']['addresses']) == 1:
            address = building['properties']['addresses'][0]
        else:
            addresses.extend(building['properties']['addresses'])
        appendBuilding(building, address, osmXml)
    if (len(addresses) > 0):
        for address in addresses:
            node = appendNewNode(address['geometry']['coordinates'], osmXml)
            appendAddress(address, node)
            
    with open(osmOut, 'w') as outFile:
        outFile.writelines(tostring(osmXml, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        print "Exported " + osmOut

getcontext().prec = 16
# Run conversions. Expects an chunks/addresses-[district id].shp for each
# chunks/buildings-[district id].shp. Optinally convert only one election district.
if (len(argv) == 2):
    convert(
        merge('chunks/buildings-%s.shp' % argv[1],
            'chunks/addresses-%s.shp' % argv[1]),
        'osm/buildings-addresses-%s.osm' % argv[1])
else:
    buildingFiles = glob("chunks/buildings-*.shp")
    for buildingFile in buildingFiles:
        matches = re.match('^.*-(\d+)\.shp$', buildingFile).groups(0)
        convert(
            merge(buildingFile,
                'chunks/addresses-%s.shp' % matches[0]),
            'osm/buildings-addresses-%s.osm' % matches[0])

# profiling
prW.disable()
ps = pstats.Stats(prW)
ps.sort_stats('time')
a = ps.print_stats(10)
