"""
MediaWiki CDB reader test module.
"""


import unittest
from mediawikicdb import mediawikixmlparser, wikiinfo, mediawikicdbwriter, wikicdbreader
from mediawikicdb.mediawikicdbdict import CdbDictIdFromName, CdbDictNameFromId, CdbDictPageFromId, CdbDictPageLinksFromId, CdbDictPageProjectsFromId


class MediaWikiCDBReaderTestCase(unittest.TestCase):
    """Test the wikicdbreader."""

    def setUp(self):
        """Parse the MediaWiki XML file, write it out in cdb format and initialize the cdb reader"""
        self.handler = mediawikixmlparser.parseMediaWikiXMLExport("xml/export3.xml")
        self.info = wikiinfo.WikiInfo()
        self.info.set(self.handler.pages, self.handler.pageRedirects, self.handler.templates,
                      self.handler.templateRedirects, self.handler.talkpages)
        self.info.doStuff()
        self.writer = mediawikicdbwriter.MediaWikiCdbWriter()
        self.writer.writeCdbFiles(self.info, "cdb/")
        #self.reader = wikicdbreader.WikiCdbReader("cdb/")

    def tearDown(self):
        """No tearDown required"""
        pass

    def test_getPageIdFromName(self):
        """Test getting page id from page name."""
        pageIdFromName = CdbDictIdFromName("cdb/pageIdFromName.cdb")
        for i in self.handler.pages:  # pageFromName
            expected = self.handler.pages[i]['id']
            result = pageIdFromName[i]['id']
            #result = self.reader.getPageIdFromName(i)
            self.assertEqual(result, expected)

    def test_getPageNameFromId(self):
        """Test getting page name from page id."""
        pageNameFromId = CdbDictNameFromId("cdb/pageNameFromId.cdb")
        for i in self.info.pageFromId:
            expected = self.info.pageFromId[i]['name']
            result = pageNameFromId[i]['name']
            #result = self.reader.getPageNameFromId(i)
            self.assertEqual(result, expected)

    def test_getPageFromId(self):
        """Test getting page from page id."""
        return
        pageFromId = CdbDictPageFromId("cdb/pageFromId.cdb")
        for i in self.info.pageFromId:
            pageName = self.info.pageFromId[i]['name']
            print "i:", i, pageName
            expected = self.handler.pages[pageName]
            result = pageFromId[i]
            #result = self.reader.getPageLinksFromId(i)
            self.assertEqual(result, expected)
        #self.assertTrue(False)

    def test_getPageLinksFromId(self):
        """Test getting page links from page id."""
        return
        pageLinksFromId = CdbDictPageLinksFromId("cdb/pageLinksFromId.cdb")
        for i in self.info.pageFromId:
            result = pageLinksFromId[i]
            #result = self.reader.getPageLinksFromId(i)
            print "links:", result
        #self.assertTrue(False)

    def test_getPageProjectsFromId(self):
        """Test getting page projects from page id."""
        return
        pageProjectsFromId = CdbDictPageProjectsFromId("cdb/pageProjectsFromId.cdb")
        for i in self.info.pageFromId:
            expected = self.info.pageFromId[i]
            result = pageProjectsFromId[i]
            #result = self.reader.getPageProjectsFromId(i)
            print "projects:", result
            self.assertEqual(result, expected)
        #self.assertTrue(False)

    def test_getProjectIdFromName(self):
        """Test getting project id from project name."""
        projectIdFromName = CdbDictIdFromName("cdb/projectIdFromName.cdb")
        for i in self.handler.templates:
            expected = self.handler.templates[i]['id']
            result = projectIdFromName[i]['id']
            #result = self.reader.getProjectIdFromName(i)
            self.assertEqual(result, expected)

    def test_getProjectNameFromId(self):
        """Test getting project name from project id."""
        projectNameFromId = CdbDictNameFromId("cdb/projectNameFromId.cdb")
        for i in self.info.templateFromId:
            print "projectId:", i, "projectName:", self.info.templateFromId[i]['name']
            expected = self.info.templateFromId[i]['name']
            result = projectNameFromId[i]['name']
            #result = self.reader.getProjectNameFromId(i)
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
