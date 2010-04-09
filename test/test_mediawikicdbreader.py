"""
MediaWiki CDB reader test module.
"""


import unittest
from mediawiki2cdb import mediawikixmlparser,wikiinfo,wikicdbwriter,wikicdbreader


class MediaWikiCDBReaderTestCase(unittest.TestCase):

    def setUp(self):
        """Parse the MediaWiki XML file, write it out in cdb format and initialize the cdb reader"""
        self.handler = mediawikixmlparser.parseMediaWikiXMLExport("xml/export3.xml")
        self.info = wikiinfo.WikiInfo()
        self.info.set(self.handler.pages,self.handler.pageRedirects,self.handler.templates,self.handler.templateRedirects,self.handler.talkpages)
        self.info.doStuff()
        self.writer = wikicdbwriter.WikiCdbWriter()
        self.writer.writeCdbFiles(self.info,"cdb/")
        self.reader = wikicdbreader.WikiCdbReader("cdb/")


    def tearDown(self):
        pass


    def test_getPageIdFromName(self):
        """Test getting page id from page name."""
        for i in self.handler.pages: # pageFromName
            expected = self.handler.pages[i]['id']
            result = self.reader.getPageIdFromName(i)
            self.assertEqual(result,expected)


    def test_getPageNameFromId(self):
        """Test getting page name from page id."""
        for i in self.info.pageFromId: # pageFromId
            print "pageId:",i,"pageName:",self.info.pageFromId[i]['name']
            expected = self.info.pageFromId[i]['name']
            result = self.reader.getPageNameFromId(i)
            self.assertEqual(result,expected)


    def test_getProjectIdFromName(self):
        """Test getting project id from project name."""
        for i in self.handler.templates:
            expected = self.handler.templates[i]['id']
            result = self.reader.getProjectIdFromName(i)
            self.assertEqual(result,expected)


    def test_getProjectNameFromId(self):
        """Test getting project name from project id."""
        for i in self.info.templateFromId:
            print "projectId:",i,"projectName:",self.info.templateFromId[i]['name']
            expected = self.info.templateFromId[i]['name']
            result = self.reader.getProjectNameFromId(i)
            self.assertEqual(result,expected)


    def test_getPageLinksFromId(self):
        """Test getting page links from page id."""
        for i in self.info.pageFromId:
            result = self.reader.getPageLinksFromId(i)
            print "links:",result


    def test_getPageProjectsFromId(self):
        """Test getting page projects from page id."""
        for i in self.info.pageFromId: # pageFromId
            result = self.reader.getPageProjectsFromId(i)
            print "projects:",result


if __name__ == "__main__":
    unittest.main()