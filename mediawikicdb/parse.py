#!/usr/bin/env python
#coding=utf-8
#file: parse.py
"""
Parse
"""

from optparse import OptionParser

import sys
import time

from mediawikixmlparser import parseMediaWikiXMLExport


from wikiinfo import WikiInfo
from mediawikicdbwriter import MediaWikiCdbWriter


def parseXmlFile(fileName):
    t0 = time.time()
    handler = parseMediaWikiXMLExport(fileName)
    t1 = time.time()
    print "Time1:", t1 - t0
    sys.stderr.write("Time:" + str(t1 - t0) + "\n")

    info = WikiInfo()
    info.set(handler.pages, handler.pageRedirects, handler.templates, handler.templateRedirects, handler.talkpages)
    info.doStuff()

    t2 = time.time()
    print "Time2:", t2 - t1
    sys.stderr.write("Time:" + str(t2 - t1) + "\n")
    return info


def example_function(filename, cdbdir):
    """
    Example function.

    Keyword arguments:
    file -- the return value

    """
    info = parseXmlFile(filename)

    writer = MediaWikiCdbWriter()
    writer.writeCdbFiles(info, cdbdir)


def main():
    parser = OptionParser()
    #parser.add_option("-f","--file",dest="filename",help="write report to FILE",metavar="FILE")
    #parser.add_option("-d","--date",dest="date",help="published DATE",metavar="DATE")
    parser.add_option("-v", action="store_true", dest="verbose", default=False, help="print status messages to stdout")

    (options, args) = parser.parse_args()
    cdbdir = "../cdb/"
    if len(args) == 0:
        filename = "../xml/export3.xml"
    else:
        filename = args[0]
    example_function(filename, cdbdir)


if __name__ == "__main__":
    main()
