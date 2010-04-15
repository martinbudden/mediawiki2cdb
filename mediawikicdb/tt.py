#!/usr/bin/env python
#coding=utf-8
#file: tt.py
"""
Test
"""

import struct
import cdb

from optparse import OptionParser
from mediawikicdbdict import CdbDictIdFromName, CdbDictNameFromId, CdbDictPageLinksFromId, CdbDictPageProjectsFromId
from mediawikicdbwriter import MediaWikiCdbWriter
import pprint


class MyPrettyPrinter(pprint.PrettyPrinter):
	def format(self, object, context, maxlevels, level):
		if isinstance(object, long):
			return hex(object), True, False
		else:
			return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


def example_function(param):
    """
    Example function.

    Keyword arguments:
    param -- the return value

    """
    pages = {'Genetics': {'id': 4}, 'Other': {'id': 5}}
    writer = MediaWikiCdbWriter()
    writer.writeCdbIdFromName("../cdb/pageIdFromName.cdb", pages)
    pageName = "Genetics"
    pageIdFromName = cdb.init("../cdb/pageIdFromName.cdb")
    p = pageIdFromName.get(pageName)
    s = struct.Struct("<l")
    i = s.unpack(p)
    print "xx", i[0]

    d = CdbDictIdFromName("../cdb/pageIdFromName.cdb")
    print "yy", d['Genetics']

    mpp = MyPrettyPrinter()

    pageProjectsFromId = CdbDictPageProjectsFromId("../cdb/pageProjectsFromId.cdb")
    print "pageProjects"
    #print pageProjectsFromId
    #mpp.pprint(pageProjectsFromId)

    d = CdbDictNameFromId("../cdb/pageNameFromId.cdb")
    print "CdbDictNameFromId"
    print d
    print "keys"
    print d.keys()
    print "d[]"
    for i in d:
        print i, d[i]

    d = CdbDictIdFromName("../cdb/pageIdFromName.cdb")
    print "CdbDictIdFromName"
    print "keys"
    print d.keys()
    print d['Genetics']
    print "d[]"
    for i in d:
        print i, d[i]
    return
    print "d.keys()"
    for i in d.keys():
        print i, d[i]
    print "d.interkeys()"
    for k in d.iterkeys():
        print d[k]
    print "d.intervalues()"
    for v in d.itervalues():
        print v
    print "d.interitems()"
    for k, v in d.iteritems():
        print 'd[', k, '] = ', v

    return param


def main():
    parser = OptionParser()
    #parser.add_option("-f","--file",dest="filename",help="write report to FILE",metavar="FILE")
    #parser.add_option("-d","--date",dest="date",help="published DATE",metavar="DATE")
    parser.add_option("-v", action="store_true", dest="verbose", default=False, help="print status messages to stdout")

    (options, args) = parser.parse_args()
    if len(args) == 0:
        param = ""
    else:
        param = args[0]
    example_function(param)


if __name__ == "__main__":
    main()
