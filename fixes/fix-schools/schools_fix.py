
from sys import argv
import xml.parsers.expat


def ordinal(n):
    # actually adding the ordinals to numbers
    n = int(n)
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
       return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, 'th')


def ordinalize(street):
    # searches, character by character, for numbers in a string
    # adds an ordinal if it comes across any
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
    # parsing the xml nodes we're interested in
    if name in accepted:
        global current
        current = {
            'type': name,
            'attrs': attrs,
            'tags': {},
            'nds': [],
            'modified': False
        }

    if name == 'nd' and current:
        global current
        current['nds'].append(attrs['ref'])

    if name == 'tag' and current:
        tag(attrs)

def tag(attrs):
    global current
    global bandera  
    for attr in attrs:
        current['tags'][attrs['k']] = attrs['v']
    if attrs['k']=='amenity' and attrs['v']=='school':
        bandera=True
    if attrs['k'] == 'building' and attrs['v']=='yes' and bandera:
        current['tags'][attrs['k']] = 'school'   	
        current['modified'] = True
        bandera=False


def end_element(name):
    # appropriate actions for closing xml nodes we used
    if name == 'osm':
        closeFile()

    if name in accepted:
        if current and current['modified']:
            addToFile(current)
            print current


def startOsmChange():
    return '<osmChange version="0.6" generator="ordinal_fixes.py"><modify>'


def endOsmChange():
    return '</modify></osmChange>'


def addToFile(item):
    global itemCount
    if itemCount >= groupLimit:
        if type(currentFile) is file:
            closeFile()
        newFile()
        itemCount = 0

    currentFile.write(xmlizeItem(item) + '\n')
    itemCount += 1


def xmlizeItem(item):
    xml = '<' + item['type']
    
    for attr in item['attrs']:
        if attr not in ['timestamp', 'user', 'uid', 'changeset', 'visible']:
            xml += ' ' + attr + '="' + item['attrs'][attr] + '"'
    xml += '>'

    if item['type'] == 'way':
        for nd in item['nds']:
            xml += '<nd ' + 'ref="' + nd + '"/>'

    for tag in item['tags']:
        xml += '<tag k="' + tag + '" v="' + item['tags'][tag] + '"/>'

    xml += '</' + item['type'] + '>'

    return xml


def newFile():
    global fileCount
    fileCount += 1
    global currentFile
    currentFile = open(argv[1].split( '.')[0]+'_fixed_' + str(fileCount) + '.osc', 'w')
    currentFile.write(startOsmChange())
    print str(groupLimit * fileCount) + ' items'


def closeFile():
    currentFile.write(endOsmChange())
    currentFile.close()


groupLimit = 2000
current = {}
currentFile = False
out = ''
accepted = ['way']
itemCount = groupLimit + 1
fileCount = 0
relations = []
bandera=False
contador =0


p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.ParseFile(open(argv[1], 'r'))

# list of relations that needs to be fixed manually
# there's not many, quicker to just do it than get clever about it
print '---------------'
print 'relations:'
print relations
