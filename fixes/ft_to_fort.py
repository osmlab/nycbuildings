# original overpass query
# <union>
#   <query type="way">
#     <has-kv k="addr:street" regv="^Ft "/>
#     <bbox-query {{bbox}}/>
#   </query>
#   <query type="way">
#   <has-kv k="name" regv="^Ft "/>
#   <bbox-query {{bbox}}/>
#   </query>
# </union>
# <union>
#   <item/>
#   <recurse type="down"/>
# </union>
# <print mode="meta"/>

from sys import argv, exit
from lxml import etree

filename = argv[1] if (len(argv) > 1) else exit('Invalid file name')
tree = etree.parse(filename)
tree = tree.getroot()
addr_streets = tree.findall(".//tag[@k='addr:street']")

counts = {};

for addr_street in addr_streets:
    name = addr_street.get('v')
    if name[0:3] == 'Ft ':
        name = 'Fort ' + name[3:]
        key = addr_street.get('v') + ' -> ' + name
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1
        addr_street.set('v', name)
        parent = addr_street.getparent()
        parent.attrib['action'] = 'modify'

for name in counts:
    print str(counts[name]) + ' ' + name

xml = "<?xml version='1.0' encoding='UTF-8'?>\n" + etree.tostring(tree, encoding='utf8')
new_file = open(filename[:-4] + '_new' + filename[-4:], 'w')
new_file.write(xml)
