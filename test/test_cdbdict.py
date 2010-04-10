"""
MediaWiki CDB dictionary test module.
"""

import unittest
from mediawikicdb.mediawikicdbdict import CdbDictIdFromName, CdbDictNameFromId, CdbDictPageLinksFromId, CdbDictPageProjectsFromId


class MediaWikiCDBDictTestCase(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_pageFromId(self):
        """Test page ids"""
        pageIdFromName = CdbDictIdFromName("cdb/pageIdFromName.cdb")
        pageNameFromId = CdbDictNameFromId("cdb/pageNameFromId.cdb")
        for i in pageNameFromId:
            name = pageNameFromId[i]
            id = pageIdFromName[name]
            #print "pagei",i,"id",id,"name",name
            self.assertEqual(i,id)


    def test_pageFromName(self):
        """Test page names"""
        pageIdFromName = CdbDictIdFromName("cdb/pageIdFromName.cdb")
        pageNameFromId = CdbDictNameFromId("cdb/pageNameFromId.cdb")
        for i in pageIdFromName:
            id = pageIdFromName[i]
            name = pageNameFromId[id]
            #print "pagei",i,"id",id,"name",name
            self.assertEqual(i,name)


    def test_projectFromId(self):
        """Test project ids"""
        projectIdFromName = CdbDictIdFromName("cdb/projectIdFromName.cdb")
        projectNameFromId = CdbDictNameFromId("cdb/projectNameFromId.cdb")
        for i in projectNameFromId:
            name = projectNameFromId[i]
            id = projectIdFromName[name]
            #print "proji",i,"id",id,"name",name
            self.assertEqual(i,id)


    def test_projectFromName(self):
        """Test project names"""
        projectIdFromName = CdbDictIdFromName("cdb/projectIdFromName.cdb")
        projectNameFromId = CdbDictNameFromId("cdb/projectNameFromId.cdb")
        for i in projectIdFromName:
            id = projectIdFromName[i]
            name = projectNameFromId[id]
            #print "proji",i,"id",id,"name",name
            self.assertEqual(i,name)


    def test_pageLinksFromId(self):
        """Test page links"""
        pageLinksFromId = CdbDictPageLinksFromId("cdb/pageLinksFromId.cdb")
        pageNameFromId = CdbDictNameFromId("cdb/pageNameFromId.cdb")
        print "links"
        for i in pageLinksFromId:
            links = pageLinksFromId[i]
            name = pageNameFromId[i]
            print "id:",i,"name:",name,"links:",links
        #self.assertTrue(False)


    def test_pageProjectsFromId(self):
        """Test page projects"""
        pageProjectsFromId = CdbDictPageProjectsFromId("cdb/pageProjectsFromId.cdb")
        pageNameFromId = CdbDictNameFromId("cdb/pageNameFromId.cdb")
        projectNameFromId = CdbDictNameFromId("cdb/projectNameFromId.cdb")
        print "projects"
        for i in pageProjectsFromId:
            projects = pageProjectsFromId[i]
            name = pageNameFromId[i]
            print "id:",i,"name:",name#,"projects:",projects
            for j in projects:
                print projectNameFromId[j],projects[j]
            print
        #self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()