from sys import argv, exit
import xml.parsers.expat

# argv[1] = filename
# argv[2] = changeset
    # osmchange need to be tagged with the open changeset the file is going in

# stretch, both osmchange and modified osm

def ordinal(n):
    n = int(n)
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
       return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, 'th')


def ordinalize(street):
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
    if name in accepted:
        global current
        current = {
            'name': name,
            'attrs': attrs,
            'tags': [],
            'nds': [],
            'modified': False
        }

    if name == 'nd':
        global current
        current['nds'].append(attrs)

    if name == 'tag':
        tag(attrs)


def tag(attrs):
    global current
    current['tags'].append(attrs)
    print current

    if attrs['k'] == 'addr:street':
        current['tags']['addr:street'] = ordinalize(attrs['v'])
        if current['tags']['addr:street'] != attrs['v']:
            current['modified'] = True
            current['version'] = str(int(current['version']) + 1)


def end_element(name):
    if name == 'osm':
        global out
        out += '</modify></osmChange>'
        print out

    if name in accepted:
        if current['modified']:
            global count
            count += 1
            addToFile(current, 'ordinal_fixed_' + count + '.osc')
            sys.exit(1)


def addToFile(item, filename):
    print item
    print filename


current = {}
out = '<osmChange version="0.6" generator="ordinal_fixes.py"><modify>'
# changeset = argv[2]
accepted = ['node', 'way', 'relation']
count = 0

p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element

p.ParseFile(open(argv[1], 'r'))


# save the entire structure of an object until the end of the element
# save a list of all used nodes in a particular group
# ability to create arbitrarily group sizes, based on count
