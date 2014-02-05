from sys import argv
import xml.parsers.expat


def fix_padding(housenum):
    addr = housenum.split('-')
    if len(addr) == 2 and addr[0].isdigit() and addr[1].isdigit():
        housenum = str(int(addr[0])) + '-' + str(int(addr[1])).zfill(2)
    return housenum


def start_element(name, attrs):
    # parsing the xml nodes we're interested in
    if name in accepted:
        global current
        if (int(attrs['timestamp'][0:4]) > 2012 and
            int(attrs['timestamp'][5:7]) > 9):
            current = {
                'type': name,
                'attrs': attrs,
                'tags': {},
                'nds': [],
                'modified': False
            }
        else:
            current = False

    if name == 'nd' and current:
        global current
        current['nds'].append(attrs['ref'])

    if name == 'tag' and current:
        tag(attrs)


def tag(attrs):
    # modifing the addr:housenumber tags we want
    global current
    for attr in attrs:
        current['tags'][attrs['k']] = attrs['v']

    if attrs['k'] == 'addr:housenumber':
        current['tags']['addr:housenumber'] = fix_padding(attrs['v'])
        if current['tags']['addr:housenumber'] != attrs['v']:
            if current['type'] == 'relation':
                # not going to build out relations right now
                # do them manually
                global relations
                relations.append(current['attrs']['id'])
                current = False
            else:
                current['modified'] = True


def end_element(name):
    # appropriate actions for closing xml nodes we used
    if name == 'osm':
        closeFile()

    if name in accepted:
        if current and current['modified']:
            addToFile(current)


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
    currentFile = open('padding_fix' + str(fileCount) + '.osc', 'w')
    currentFile.write(startOsmChange())
    print str(groupLimit * fileCount) + ' items'


def closeFile():
    currentFile.write(endOsmChange())
    currentFile.close()


groupLimit = 2500
current = {}
currentFile = False
out = ''
accepted = ['node', 'way', 'relation']
itemCount = groupLimit + 1
fileCount = 0
relations = []


p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.ParseFile(open(argv[1], 'r'))

# list of relations that needs to be fixed manually
# there's not many, quicker to just do it than get clever about it
print '---------------'
print 'relations:'
print relations
