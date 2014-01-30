from sys import argv, exit
import xml.parsers.expat

theglobal = {}
out = '<osmChange version="0.6" generator="ordinal_fixes.py"><modify>'
count = 0
file_count = 0

def ordinal(n):
    n = int(n)
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
       return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, 'th')

def replace(street):
    for index, char in enumerate(street):
        if char.isdigit():
            start = index
            end = index

            while end < len(street) and street[end].isdigit():
                end += 1
            number = street[start:end]

            if street[start+end:end+1].isspace():
                street = ordinal(number) + street[0:start] + street[end:]

    return street

def start_element(name, attrs):
    accepted = ['node', 'way', 'relation']
    if name in accepted:
        global theglobal
        theglobal['name'] = name
        theglobal['attrs'] = attrs

    global count
    if (name == 'tag' and
        'k' in attrs and
        attrs['k'] == 'addr:street'):
            new_street = replace(attrs['v'])
            if attrs['v'] != new_street:
                count += 1
                if theglobal and theglobal['name']:
                    global out
                    out += '<' + theglobal['name']
                    for attr in theglobal['attrs']:
                        if attr != 'version':
                            out += ' ' + attr + '="' + theglobal['attrs'][attr] + '"'
                    out += '><tag k="addr:street" v="' + new_street + '"/>'
                    out += '</' + theglobal['name'] + '>'
                theglobal = {}

    if count > 2000:
        global file_count
        file_count += 1
        new_file = open('fix_ordinals_' + file_count + '.osc', 'w')
        new_file.write(xml)

    # if over 2000, create new file, etc..

def end_element(name):
    if name == 'osm':
        global out
        out += '</modify></osmChange>'
        print out

openEle = False

p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element

p.ParseFile(open('nyc.osm', 'r'))
