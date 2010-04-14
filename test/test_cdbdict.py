"""
MediaWiki CDB dictionary test module.
"""

import unittest
from mediawikicdb.mediawikicdbdict import CdbDict, CdbDictIdFromName, CdbDictNameFromId, CdbDictPageFromId, CdbDictPageLinksFromId, CdbDictPageProjectsFromId


class MediaWikiCDBDictTestCase(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_pageCdbDict(self):
        d = CdbDict("cdb/pageIdFromName.cdb");

        # test __iter__
        try:
            for i in d:
                pass
        except NotImplementedError:
            pass

        # test __getitem__
        try:
            v = d[0]
        except NotImplementedError:
            pass

        # test keys()
        try:
            keys = d.keys()
        except NotImplementedError:
            pass

        # test __delitem__
        try:
            del d[0]
        except TypeError:
            pass

        # test __setitem__
        try:
            d[0] = 0
        except TypeError:
            pass

    def test_pageNameFromId(self):
        """Test page ids"""
        pageIdFromName = CdbDictIdFromName("cdb/pageIdFromName.cdb")
        pageNameFromId = CdbDictNameFromId("cdb/pageNameFromId.cdb")
        for i in pageNameFromId:
            name = pageNameFromId[i]
            print "name:",name
            id = pageIdFromName[name['name']]['id']
            #print "pagei",i,"id",id,"name",name
            self.assertEqual(i,id)

        # test iter
        i = pageIdFromName.__iter__()
        self.assertEqual(i,i.__iter__())

        # test keys
        result = pageIdFromName.keys()
        expected = ['A', 'B', 'Genetics', 'Biochemistry', '\xc3\x86', 'EBay', 'Cell nucleus', '\xc3\x9f', 'Deoxyribonuclease I', 'DNA']
        #self.assertEqual(result,expected)
        result = pageNameFromId.keys()
        expected = [290, 3783, 12266, 198274, 5507057, 3954, 7955, 184309, 6235, 130495]
        #self.assertEqual(result,expected)


    def test_pageIdFromName(self):
        """Test page names"""
        pageIdFromName = CdbDictIdFromName("cdb/pageIdFromName.cdb")
        pageNameFromId = CdbDictNameFromId("cdb/pageNameFromId.cdb")
        return
        for i in pageIdFromName:
            id = pageIdFromName[i]
            print "pagei",i,"id",id
            name = pageNameFromId[id]
            print "pagei",i,"id",id,"name",name
            self.assertEqual(i,name)
        self.assertTrue(False)


    def test_projectNameFromId(self):
        """Test project ids"""
        projectIdFromName = CdbDictIdFromName("cdb/projectIdFromName.cdb")
        projectNameFromId = CdbDictNameFromId("cdb/projectNameFromId.cdb")
        return
        for i in projectNameFromId:
            name = projectNameFromId[i]
            id = projectIdFromName[name]
            #print "proji",i,"id",id,"name",name
            self.assertEqual(i,id)


    def test_projectIdFromName(self):
        """Test project names"""
        return
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
        return
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
        return
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