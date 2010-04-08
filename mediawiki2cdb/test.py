#!/usr/bin/env python
#coding=utf-8
#file: test.py
"""
Test
"""

from optparse import OptionParser

import pprint

from wikicdbreader import WikiCdbReader
from wikicdbwriter import WikiCdbWriter
from mediawikixmltocdb import parseXmlFile


class MyPrettyPrinter(pprint.PrettyPrinter):
	def format(self, object, context, maxlevels, level):
		if isinstance(object, long):
			return hex(object), True, False
		else:
			return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


def printOutput(handler):
	print "====Output==="
	mpp = MyPrettyPrinter()
	#print "\npages:"
	#mpp.pprint(handler.pages)
	
	print "\npageRedirects:"
	mpp.pprint(handler.pageRedirects)
	#print "\ntalkpages:"
	#mpp.pprint(handler.talkpages)
	print "\ntemplates:"
	mpp.pprint(handler.templates)
	print "\ntemplateRedirects:"
	mpp.pprint(handler.templateRedirects)


def printOutputIds(handler):
	mpp = MyPrettyPrinter()
	#print "\npageIds:"
	#mpp.pprint(handler.pageIds)
	print "\ntemplateIds:"
	mpp.pprint(handler.templateIds)


def printPage(handler,pageName):
	mpp = MyPrettyPrinter()
	page = handler.pages[pageName]

	#print "\npage: " + pageName + ":"
	#mpp.pprint(page)

	print "\npageId: " + pageName + ":"
	mpp.pprint(handler.pageIds[page['id']])
	#print "\ntalk: " + pageName + ":"
	#mpp.pprint(handler.talkpages[pageName])
	#print "\ntalkpages:"
	#mpp.pprint(handler.talkpages)


def readCdbs(projectName,pageName):
	reader = WikiCdbReader()
	reader.printCdbFile("../cdb/projects.cdb")
	reader.printCdbFile("../cdb/pages.cdb")
	reader.printCdbIdFile("../cdb/projectIds.cdb")
	if projectName:
		print "\n\n"
		print "Project:" + projectName
		projectId = reader.getProjectId(projectName)
		print "ProjectId:"+hex(projectId)
		print "ProjectName:"+reader.getProjectName(projectId)
		print "\n\n"
	print "Page:" + pageName
	pageId = reader.getPageId(pageName)
	print "PageId:"+hex(pageId)
	print "PageName:"+reader.getPageName(pageId)
	print "PageLinks:"
	mpp = MyPrettyPrinter()
	mpp.pprint(reader.getPageLinks(pageId))
	print "PageProjects:"
	mpp.pprint(reader.getPageProjects(pageId))
	print "\n\n"


def example_function(param):
    """
    Example function.

    Keyword arguments:
    param -- the return value

    """
    #pageName = "Algeria"
    #parseXmlFile("../../enwiki/enwiki-20081008-pages-meta-current.xml")
    #readCdbs(None,pageName)
    #reader = WikiCdbReader()
    pageName = "Cell nucleus"
    info = parseXmlFile("../xml/export3.xml")
    printOutput(info)
    printOutputIds(info)
    printPage(info,pageName)

    writer = WikiCdbWriter()
    writer.writeCdbFiles(info)
    readCdbs("EvolWikiProject",pageName)

    #pageName = "ß"
    #parseXmlFile("../xml/export3.xml",pageName)
    #readCdbs("../cdb/WP Writing systems",pageName)
    return param


def main():
    parser = OptionParser()
    #parser.add_option("-f","--file",dest="filename",help="write report to FILE",metavar="FILE")
    #parser.add_option("-d","--date",dest="date",help="published DATE",metavar="DATE")
    parser.add_option("-v", action="store_true", dest="verbose", default=False, help="print status messages to stdout")

    (options,args) = parser.parse_args()
    if len(args) == 0:
        param = ""
    else:
        param = args[0]
    example_function(param)


if __name__ == "__main__":
    main()
