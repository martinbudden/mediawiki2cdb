"""
MediaWiki Info test module.
"""


import unittest
from mediawikicdb import mediawikixmlparser,wikiinfo


class MediaWikiInfoTestCase(unittest.TestCase):

    def setUp(self):
        """Parse the mediawiki XML file"""
        self.handler = mediawikixmlparser.parseMediaWikiXMLExport("xml/export3.xml")
        self.info = wikiinfo.WikiInfo()
        self.info.set(self.handler.pages,self.handler.pageRedirects,self.handler.templates,self.handler.templateRedirects,self.handler.talkpages)
        self.info.doStuff()


    def tearDown(self):
        pass


    def test_pageFromId(self):
        """Test page ids"""
        for i in self.info.pageFromId:
            name = self.info.pageFromId[i]['name']
            id = self.info.pages[name]['id']
            #print "i",i,"id",id,"name",name
            self.assertEqual(i,id)


    def test_templateFromId(self):
        """Test template ids"""
        for i in self.info.templateFromId:
            name = self.info.templateFromId[i]['name']
            id = self.info.templates[name]['id']
            #print "i",i,"id",id,"name",name
            self.assertEqual(i,id)


if __name__ == "__main__":
    unittest.main()
