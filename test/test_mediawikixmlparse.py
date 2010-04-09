"""
WikiInfo test module.
"""

"""
WikiInfo test module.
"""

import unittest
from mediawiki2cdb import mediawikixmltocdb
from mediawiki2cdb import test


class WikiInfoTestCase(unittest.TestCase):

    def setUp(self):
        self.info = mediawikixmltocdb.parseXmlFile("xml/export3.xml")

    def tearDown(self):
        pass

    def testExample(self):
        """Test example function."""
        print "====testing===="
        result = True
        expected = True
        self.assertEqual(result, expected)
        self.assertTrue(result)
        test.printOutput(self.info)
        self.assertTrue(False)




if __name__ == "__main__":
    unittest.main()