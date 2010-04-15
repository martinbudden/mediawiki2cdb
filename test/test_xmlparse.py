"""
MediaWiki XML parser test module.
"""


import unittest
from mediawikicdb import mediawikixmlparser
from mediawikicdb import test


class MediaWikiXMLParserTestCase(unittest.TestCase):

    def setUp(self):
        """Parse the mediawiki XML file"""
        self.handler = mediawikixmlparser.parseMediaWikiXMLExport("xml/export3.xml")
        self.pages = { \
            'A': {'id': 290}, \
            'B': {'id': 3783}, \
            'Genetics': {'id': 12266}, \
            'Biochemistry': {'id': 3954}, \
            'EBay': {'id': 130495}, \
            'Cell nucleus': {'id': 6235}, \
            'Deoxyribonuclease I': {'id': 5507057}, \
            'DNA': {'id': 7955}}
            #'Messenger RNA':{'id':20232}, \
            #'Mitochondrion':{'id':19588}, \
            #'Ribosome':{'id':25766}, \
            #'RNA':{'id':25758}, \
            #'RNA splicing':{'id':28524}, \
            #'\xc3\x86':{'id':184309}, \
            #'\xc3\x9f':{'id':198274}, \

        self.pageRedirects = {'Dna': {'id': 0x1f14L, 'redirect': u'DNA'}, \
            'Messenger rna': {'id': 0xacee79L, 'redirect': u'Messenger RNA'}, \
            'Mitochondria': {'id': 0x4999L, 'redirect': u'Mitochondrion'}, \
            'Ribosomes': {'id': 0xf3c59L, 'redirect': u'Ribosome'}, \
            'Rna': {'id': 0x4f2f89L, 'redirect': u'RNA'}, \
            'Rna splicing': {'id': 0x4e3056L, 'redirect': u'RNA splicing'}} \

        self.templates = {'Chemicals': {'id': 3254420}, \
            'Chemistry': {'id': 1715089}, \
            'EvolWikiProject': {'id': 642240}, \
            'Physics': {'id': 3586869}, \
            'WP Writing systems': {'id': 0x6159d9L}, \
            'WP1.0': {'id': 10128391}, \
            'WPMED': {'id': 6757468}, \
            'WikiProject Biology': {'id': 10935260}, \
            'WikiProject Genetics': {'id': 17283566}, \
            'WikiProject Molecular and Cellular Biology': {'id': 6709323}, \
            'WikiProject Plants': {'id': 7890568}, \
            'WikiProjectBanners': {'id': 9320556}}

        self.templateRedirects = {'Biology': {'id': 0xa8a31aL, 'redirect': u'WikiProject Biology'}, \
            'Cell Signaling Project': {'id': 0x533c23L, 'redirect': u'WikiProject Cell Signaling'}, \
            'Wikiproject Evolution': {'id': 0x11b555cL, 'redirect': u'EvolWikiProject'}, \
            'Wikiproject Genetics': {'id': 0x1082647L, 'redirect': u'WikiProject Genetics'}, \
            'Wikiproject MCB': {'id': 0x1079802L, 'redirect': u'WikiProject Molecular and Cellular Biology'}, \
            'Wikiproject mcb': {'id': 0x98b40dL, 'redirect': u'WikiProject Molecular and Cellular Biology'}} \


    def tearDown(self):
        pass

    def test_pages(self):
        """Test pages"""
        result = self.handler.pages
        expected = self.pages
        for i in expected:
            self.assertEqual(result[i]['id'], expected[i]['id'])

    def test_pageRedirects(self):
        """Test pageRedirects"""
        result = self.handler.pageRedirects
        expected = self.pageRedirects
        self.assertEqual(result, expected)

    def test_templates(self):
        """Test pages"""
        result = self.handler.templates
        expected = self.templates
        self.assertEqual(result, expected)

    def test_templateRedirects(self):
        """Test pages"""
        result = self.handler.templateRedirects
        expected = self.templateRedirects
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
