#!/usr/bin/env python
#coding=utf-8
#file: test.py
"""
Test
"""

from optparse import OptionParser

import pprint

from mediawikicdbwriter import MediaWikiCdbWriter
from wikicdbreader import MediaWikiCdbReader
from parse import parseXmlFile


class MyPrettyPrinter(pprint.PrettyPrinter):
	def format(self, object, context, maxlevels, level):
		if isinstance(object, long):
			return hex(object), True, False
		else:
			return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


def printOutput(handler):
	print "====Output2==="
	mpp = MyPrettyPrinter()
	print "\npages:"
	#mpp.pprint(handler.pages)
	for p in handler.pages:
		print "'"+p+"':{'id':"+str(handler.pages[p]['id'])+"},"

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
	#print "\ntemplateIds:"
	#mpp.pprint(handler.templateIds)


def printPage(handler,pageName):
	mpp = MyPrettyPrinter()
	page = handler.pages[pageName]

	#print "\npage: " + pageName + ":"
	#mpp.pprint(page)

	#print "\npageId: " + pageName + ":"
	#mpp.pprint(handler.pageIds[page['id']])
	#print "\ntalk: " + pageName + ":"
	#mpp.pprint(handler.talkpages[pageName])
	#print "\ntalkpages:"
	#mpp.pprint(handler.talkpages)


def readCdbs(projectName,pageName):
	reader = MediaWikiCdbReader("../cdb/")
	reader.printCdbFromNameFile("../cdb/projectIdFromName.cdb")
	reader.printCdbFromNameFile("../cdb/pageIdFromName.cdb")
	reader.printCdbFromIdFile("../cdb/projectNameFromId.cdb")
	if projectName:
		print "\n\n"
		print "Project:" + projectName
		projectId = reader.getProjectIdFromName(projectName)
		print "ProjectId:"+hex(projectId)
		print "ProjectName:"+reader.getProjectNameFromId(projectId)
		print "\n\n"
	print "Page:" + pageName
	pageId = reader.getPageIdFromName(pageName)
	print "PageId:"+hex(pageId)
	print "PageName:"+reader.getPageNameFromId(pageId)
	print "PageLinks:"
	mpp = MyPrettyPrinter()
	mpp.pprint(reader.getPageLinksFromId(pageId))
	print "PageProjects:"
	mpp.pprint(reader.getPageProjectsFromId(pageId))
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
    info = parseXmlFile("../xml/export3.xml")
    printOutput(info)
    printOutputIds(info)
    pageName = "Cell nucleus"
    printPage(info,pageName)

    writer = MediaWikiCdbWriter()
    writer.writeCdbFiles(info,"../cdb/")
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
