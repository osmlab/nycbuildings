from fiona import collection
from sys import argv
from glob import glob

if (len(argv) == 2):
    addrs = glob("chunks/addresses-%s.shp")
    for addr in addrs:
        print addr
else:
    addrs = glob("chunks/addresses*.shp")
    for addr in addrs:
        try:
            with collection(addr, "r") as input:
                for address in input:
                    if 'properties' in address and 'STREET_NAM' in address['properties']:
                        if address['properties']['STREET_NAM'].lower().startswith('ft '):
                            print 'possible FORT: ' + address['properties']['STREET_NAM']
        except Exception, e:
            print 'error with ' + addr