from sys import argv, exit
from lxml import etree

def ordinal(n):
    n = int(n)
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
       return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, 'th')

filename = argv[1] if (len(argv) > 1) else exit('Invalid file name')
tree = etree.parse(filename)
addr_streets = tree.findall(".//tag[@k='addr:street']")

for addr_street in addr_streets:
  name = addr_street.get('v')

  for index, char in enumerate(name):
    if char.isdigit():
        start = index
        end = index
        while end < len(name) and name[end].isdigit():
            end += 1
        number = name[start:end]

        if name[start+end:end+1].isspace():
            name = ordinal(number) + name[0:start] + name[end:]

        if name != addr_street.get('v'):
            print  '- %s > %s' % (addr_street.get('v'), name)
            addr_street.set('v', name)
            parent = addr_street.getparent()
            parent.attrib['action'] = 'modify'

xml = "<?xml version='1.0' encoding='UTF-8'?>\n" + etree.tostring(tree, encoding='utf8').replace('"',"'")
new_file = open(filename[:-4] + '_new' + filename[-4:], 'w')
new_file.write(xml)
