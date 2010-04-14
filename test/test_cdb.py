"""
CDB test module.
"""

import unittest
import os
from mediawikicdb import mediawikicdbwriter
from mediawikicdb.mediawikicdbdict import CdbDict, CdbDictIntKey, CdbDictIdFromName, CdbDictNameFromId, CdbDictPageFromId, CdbDictPageLinksFromId, CdbDictPageProjectsFromId


#{'':,'name':'','class':,'importance':,'links':{set()},'projects':{{'':,'class':,'importance':}}


class CDBTestCase(unittest.TestCase):

    def setUp(self):
        self.dir = "testcdb/"
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)


    def tearDown(self):
        pass


    def test_intKey(self):
        """Test page int key"""
        testPages = { \
            290:'A',
            3783:'B',
            12266:'Genetics',
            3954:'Biochemistry',
            130495:'EBay',
            6235:'Cell nucleus',
            5507057:'Deoxyribonuclease I',
            7955:'DNA'}
        pageIntFromName = CdbDictIntKey(self.dir+"pageIntFromName.cdb")
        pageIntFromName.clear()
        pageIntFromName.update(testPages)
        self.assertEqual(len(pageIntFromName),len(testPages))

        for i in testPages:
            expected = testPages[i]
            result = pageIntFromName[i]
            self.assertEqual(result,expected)
        pageIntFromName.clear()
        self.assertEqual(len(pageIntFromName),0)


    def test_idFromName(self):
        """Test page id from name"""
        testPages = { \
            'A':{'id':290},
            'B':{'id':3783},
            'Genetics':{'id':12266},
            'Biochemistry':{'id':3954},
            'EBay':{'id':130495},
            'Cell nucleus':{'id':6235},
            'Deoxyribonuclease I':{'id':5507057},
            'DNA':{'id':7955}}
        #writer = mediawikicdbwriter.MediaWikiCdbWriter()
        #writer.writeCdbIdFromName(self.dir+"pageIdFromName.cdb",testPages)
        pageIdFromName = CdbDictIdFromName(self.dir+"pageIdFromName.cdb")
        pageIdFromName.clear()
        pageIdFromName.update(testPages)

        for i in testPages:
            expected = testPages[i]
            result = pageIdFromName[i]
            print "r,e",result,expected
            self.assertEqual(result,expected)
        pageIdFromName.clear()
        self.assertEqual(len(pageIdFromName.keys()),0)


    def test_idFromName2(self):
        """Test page id from name"""
        return
        testPages = { \
            'A':{'id':290},
            'B':{'id':3783},
            'Genetics':{'id':12266},
            'Biochemistry':{'id':3954},
            'EBay':{'id':130495},
            'Cell nucleus':{'id':6235},
            'Deoxyribonuclease I':{'id':5507057},
            'DNA':{'id':7955}}
        writer = mediawikicdbwriter.MediaWikiCdbWriter()
        writer.writeCdbIdFromName(self.dir+"pageIdFromName.cdb",testPages)
        pageIdFromName = CdbDictIdFromName(self.dir+"pageIdFromName.cdb")

        pageIdFromName['D'] = {'id':1234}
        testPages['D'] = {'id':1234}
        for i in testPages:
            expected = testPages[i]
            result = pageIdFromName[i]
            self.assertEqual(result,expected)

        testPages['E'] = {'id':1235}
        testPages['F'] = {'id':1236}
        pageIdFromName.update({'E':1235,'F':1236})
        for i in testPages:
            print "bb",i
            expected = testPages[i]['id']
            result = pageIdFromName[i]
            self.assertEqual(result,expected)

        self.assertTrue(False)


    def test_nameFromId(self):
        """Test page id from name"""
        testPages = { \
             290:{'name':'A'},
             3783:{'name':'B'},
             12266:{'name':'Genetics'},
             3954:{'name':'Biochemistry'},
             130495:{'name':'EBay'},
             6235:{'name':'Cell nucleus'},
             5507057:{'name':'Deoxyribonuclease I'},
             7955:{'name':'DNA'}}
        writer = mediawikicdbwriter.MediaWikiCdbWriter()
        writer.writeCdbNameFromId(self.dir+"pageNameFromId.cdb",testPages)
        pageNameFromId = CdbDictNameFromId(self.dir+"pageNameFromId.cdb")
        for i in testPages:
            expected = testPages[i]
            result = pageNameFromId[i]
            self.assertEqual(result,expected)


    def test_pages(self):
        """Test page id from name"""
        testPages = { \
             #   {'name':'','class':1,'importance':2,'links':set(4,5,6),'projects':{{'100':,'class':8,'importance':9}}
             290:{'name':'A','class':1,'importance':2,'links':set([4,5,6]),'projects':{100:{'class':8,'importance':9}}},
             3783:{'name':'B','class':4,'importance':5,'links':set([1,2,3]),'projects':{200:{'class':2,'importance':3}}},
             4783:{'name':'C','class':6,'importance':7,'links':set([]),'projects':{}},
             4783:{'name':'D','class':9,'importance':4,'links':set([9,100,1001]),'projects':{}},
             5783:{'name':'DEF','class':2,'importance':1,'links':set([1,2,3,4,5,6]),'projects':{200:{'class':2,'importance':3},300:{'class':3,'importance':4},400:{'class':4,'importance':5}}},
             }

        writer = mediawikicdbwriter.MediaWikiCdbWriter()
        writer.writeCdbPages(self.dir+"pageFromId.cdb",testPages)
        pageNameFromId = CdbDictPageFromId(self.dir+"pageFromId.cdb")
        for i in testPages:
            expected = testPages[i]
            result = pageNameFromId[i]
            #print "r:",result
            #print "e:",expected
            self.assertEqual(result,expected)


if __name__ == "__main__":
    unittest.main()