"""
MediaWiki CDB dictionary test module.
"""

import unittest
import os
from mediawikicdb.mediawikicdbdict import CdbDictIdFromName, CdbDictNameFromId, CdbDictPageFromId, CdbDictPageLinksFromId, CdbDictPageProjectsFromId


class MediaWikiCDBDictTestCase(unittest.TestCase):

    def setUp(self):
        self.dir = "testcdb/"
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def tearDown(self):
        pass

    def test_idFromName(self):
        """Test page id from name"""
        testPages = { \
            'A': {'id': 290},
            'B': {'id': 3783},
            'Genetics': {'id': 12266},
            'Biochemistry': {'id': 3954},
            'EBay': {'id': 130495},
            'Cell nucleus': {'id': 6235},
            'Deoxyribonuclease I': {'id': 5507057},
            'DNA': {'id': 7955}}
        #writer = mediawikicdbwriter.MediaWikiCdbWriter()
        #writer.writeCdbIdFromName(self.dir+"pageIdFromName.cdb", testPages)
        pageIdFromName = CdbDictIdFromName(self.dir + "pageIdFromName.cdb")

        # test _pack_value and _unpack_value
        expected = {'id': 12266}
        result = pageIdFromName._unpack_value(pageIdFromName._pack_value(expected))
        self.assertEqual(result, expected)

        # test _pack_key and _unpack_key
        expected = 'Genetics'
        result = pageIdFromName._unpack_key(pageIdFromName._pack_key(expected))
        self.assertEqual(result, expected)

        pageIdFromName.clear()
        pageIdFromName.update(testPages)

        for i in testPages:
            expected = testPages[i]
            result = pageIdFromName[i]
            print "r, e", result, expected
            self.assertEqual(result, expected)
        pageIdFromName.clear()
        self.assertEqual(len(pageIdFromName.keys()), 0)

    def test_nameFromId(self):
        """Test page id from name"""
        testPages = { \
             290: {'name': 'A'},
             3783: {'name': 'B'},
             12266: {'name': 'Genetics'},
             3954: {'name': 'Biochemistry'},
             130495: {'name': 'EBay'},
             6235: {'name': 'Cell nucleus'},
             5507057: {'name': 'Deoxyribonuclease I'},
             7955: {'name': 'DNA'}}
        #writer = mediawikicdbwriter.MediaWikiCdbWriter()
        #writer.writeCdbNameFromId(self.dir+"pageNameFromId.cdb", testPages)
        pageNameFromId = CdbDictNameFromId(self.dir + "pageNameFromId.cdb")

        # test _pack_value and _unpack_value
        expected = {'name': 'Genetics'}
        result = pageNameFromId._unpack_value(pageNameFromId._pack_value(expected))
        self.assertEqual(result, expected)

        # test _pack_key and _unpack_key
        expected = 12266
        result = pageNameFromId._unpack_key(pageNameFromId._pack_key(expected))
        self.assertEqual(result, expected)

        pageNameFromId.clear()
        pageNameFromId.update(testPages)
        for i in testPages:
            expected = testPages[i]
            result = pageNameFromId[i]
            self.assertEqual(result, expected)

    def test_pages(self):
        """Test page id from name"""
        testPages = { \
             290: {'name': 'A', 'class': 1, 'importance': 2, 'links': set([4, 5, 6]), 'projects': {100: {'class': 8, 'importance': 9}}},
             3783: {'name': 'B', 'class': 4, 'importance': 5, 'links': set([1, 2, 3]), 'projects': {200: {'class': 2, 'importance': -1}}},
             4783: {'name': 'C', 'class': 6, 'importance': 7, 'links': set([]), 'projects': {}},
             4783: {'name': 'D', 'class': 9, 'importance': 4, 'links': set([9, 100, 1001]), 'projects': {}},
             5783: {'name': 'DEF', 'class': 2, 'importance': 1, 'links': set([1, 2, 3, 4, 5, 6]), \
                 'projects': {200: {'class': 2, 'importance': 3}, 300: {'class': 3, 'importance': 4}, 400: {'class': 4, 'importance': 5}}},
             6783: {'name': 'GG', 'class': 0, 'importance': -1, 'links': set([9, 100, 1001]), 'projects': {}}}

        #writer = mediawikicdbwriter.MediaWikiCdbWriter()
        #writer.writeCdbPages(self.dir+"pageFromId.cdb", testPages)
        pageFromId = CdbDictPageFromId(self.dir + "pageFromId.cdb")

        # test _pack_value and _unpack_value
        expected = {'name': 'B', 'class': 4, 'importance': 5, 'links': set([1, 2, 3]), 'projects': {200: {'class': 2, 'importance': 3}}}
        result = pageFromId._unpack_value(pageFromId._pack_value(expected))
        self.assertEqual(result, expected)

        # test _pack_key and _unpack_key
        expected = 3783
        result = pageFromId._unpack_key(pageFromId._pack_key(expected))
        self.assertEqual(result, expected)

        pageFromId.clear()
        pageFromId.update(testPages)
        for i in testPages:
            expected = testPages[i]
            result = pageFromId[i]
            #print "r:", result
            #print "e:", expected
            self.assertEqual(result, expected)

    def test_pageNameFromId(self):
        """Test page ids"""
        pageIdFromName = CdbDictIdFromName("cdb/pageIdFromName.cdb")
        pageNameFromId = CdbDictNameFromId("cdb/pageNameFromId.cdb")
        for i in pageNameFromId:
            name = pageNameFromId[i]
            print "name:", name
            result = pageIdFromName[name['name']]['id']
            #print "pagei", i, "id", id, "name", name
            self.assertEqual(result, i)

        # test keys
        result = pageIdFromName.keys()
        expected = ['A', 'B', 'Genetics', 'Biochemistry', '\xc3\x86', 'EBay', 'Cell nucleus', '\xc3\x9f', 'Deoxyribonuclease I', 'DNA']
        self.assertEqual(result, expected)
        result = pageNameFromId.keys()
        expected = [290, 3783, 12266, 198274, 5507057, 3954, 7955, 184309, 6235, 130495]
        self.assertEqual(result, expected)

    def test_pageIdFromName(self):
        """Test page names"""
        return
        pageIdFromName = CdbDictIdFromName("cdb/pageIdFromName.cdb")
        pageNameFromId = CdbDictNameFromId("cdb/pageNameFromId.cdb")
        for i in pageIdFromName:
            result = pageIdFromName[i]['id']
            #print "pagei", i, "id", id
            expected = pageNameFromId[id]['name']
            #print "pagei", i, "id", id, "name", name
            self.assertEqual(result, expected)

    def test_projectNameFromId(self):
        """Test project ids"""
        projectIdFromName = CdbDictIdFromName("cdb/projectIdFromName.cdb")
        projectNameFromId = CdbDictNameFromId("cdb/projectNameFromId.cdb")
        return
        for i in projectNameFromId:
            name = projectNameFromId[i]
            ident = projectIdFromName[name]
            #print "proji", i, "id", id, "name", name
            self.assertEqual(i, ident)

    def test_projectIdFromName(self):
        """Test project names"""
        return
        projectIdFromName = CdbDictIdFromName("cdb/projectIdFromName.cdb")
        projectNameFromId = CdbDictNameFromId("cdb/projectNameFromId.cdb")
        for i in projectIdFromName:
            ident = projectIdFromName[i]
            name = projectNameFromId[ident]
            #print "proji", i, "id", id, "name", name
            self.assertEqual(i, name)

    def test_pageLinksFromId(self):
        """Test page links"""
        return
        pageLinksFromId = CdbDictPageLinksFromId("cdb/pageLinksFromId.cdb")

        # test _pack_value and _unpack_value
        expected = {1439: {'class': 3, 'importance': -1, 'links': set([4, 5, 6])}}
        result = pageLinksFromId._unpack_value(pageLinksFromId._pack_value(expected))
        self.assertEqual(result, expected)

        # test _pack_key and _unpack_key
        expected = 12266
        result = pageLinksFromId._unpack_key(pageLinksFromId._pack_key(expected))
        self.assertEqual(result, expected)

        pageNameFromId = CdbDictNameFromId("cdb/pageNameFromId.cdb")
        print "links"
        for i in pageLinksFromId:
            links = pageLinksFromId[i]
            name = pageNameFromId[i]
            print "id:", i, "name:", name, "links:", links
        #self.assertTrue(False)

    def test_pageProjectsFromId(self):
        """Test page projects"""
        return
        pageProjectsFromId = CdbDictPageProjectsFromId("cdb/pageProjectsFromId.cdb")

        # test _pack_value and _unpack_value
        expected = {1397: {'class': 4, 'importance': -1}}
        result = pageProjectsFromId._unpack_value(pageProjectsFromId._pack_value(expected))
        self.assertEqual(result, expected)

        # test _pack_key and _unpack_key
        expected = 12266
        result = pageProjectsFromId._unpack_key(pageProjectsFromId._pack_key(expected))
        self.assertEqual(result, expected)

        pageNameFromId = CdbDictNameFromId("cdb/pageNameFromId.cdb")
        projectNameFromId = CdbDictNameFromId("cdb/projectNameFromId.cdb")
        return
        print "projects"
        for i in pageProjectsFromId:
            projects = pageProjectsFromId[i]
            name = pageNameFromId[i]
            print "id:", i, "name:", name, "projects:", projects
            for j in projects:
                print projectNameFromId[j], projects[j]
            print
        #self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
