"""
CDB dictionary test module.
"""

import unittest
import os
from mediawikicdb.cdbdict import CdbDict, CdbDictIntKey, CdbDictIntValue
#from mediawikicdb import CdbDict, CdbDictIntKey, CdbDictIntValue


class CDBDictTestCase(unittest.TestCase):
    """Basic test for cdbdict."""

    def setUp(self):
        """Create directory for testing."""
        self.dir = "testcdb/"
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def tearDown(self):
        """No teardown required."""
        pass

    def test_pageCdbDict(self):
        filename = "testcdb/temp.cdb"
        if os.path.exists(filename):
            os.remove(filename)

        d = CdbDict(filename)

        # test __delitem__
        try:
            del d[0]
            self.assertTrue(False)
        except TypeError:
            pass

        # test __setitem__
        try:
            d[0] = 0
            self.assertTrue(False)
        except TypeError:
            pass

        # test iter
        i = d.__iter__()
        self.assertEqual(i, i.__iter__())

        # test _pack_value and _unpack_value
        expected = 'abcde'
        result = d._unpack_value(d._pack_value(expected))
        self.assertEqual(result, expected)

        # test _pack_key and _unpack_key
        expected = 'abcde'
        result = d._unpack_key(d._pack_key(expected))
        self.assertEqual(result, expected)

        testPages = {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'}
        d.update(testPages)

        self.assertEqual(len(d), len(testPages))
        for i in testPages:
            expected = testPages[i]
            result = d[i]
            print "i, e, r", i, expected, result
            self.assertEqual(result, expected)

        os.remove(filename)

    def test_intKey(self):
        """Test dictionary with integer key"""
        testPages = { \
            290: 'A',
            3783: 'B',
            12266: 'Genetics',
            3954: 'Biochemistry',
            130495: 'EBay',
            6235: 'Cell nucleus',
            5507057: 'Deoxyribonuclease I',
            7955: 'DNA'}
        pageIntFromName = CdbDictIntKey(self.dir + "pageIntKey.cdb")

        # test _pack_value and _unpack_value
        expected = 'abcde'
        result = pageIntFromName._unpack_value(pageIntFromName._pack_value(expected))
        self.assertEqual(result, expected)

        # test _pack_key and _unpack_key
        expected = 1234
        result = pageIntFromName._unpack_key(pageIntFromName._pack_key(expected))
        self.assertEqual(result, expected)

        pageIntFromName.clear()
        pageIntFromName.update(testPages)
        self.assertEqual(len(pageIntFromName), len(testPages))

        for i in testPages:
            expected = testPages[i]
            result = pageIntFromName[i]
            self.assertEqual(result, expected)
        pageIntFromName.clear()
        self.assertEqual(len(pageIntFromName), 0)

    def test_intValue(self):
        """Test dictionary with integer values"""
        testPages = { \
            'A': 290,
            'B': 3783,
            'Genetics': 12266,
            'Biochemistry': 3954,
            'EBay': 130495,
            'Cell nucleus': 6235,
            'Deoxyribonuclease I': 5507057,
            'DNA': 7955}
        #writer = mediawikicdbwriter.MediaWikiCdbWriter()
        #writer.writeCdbIdFromName(self.dir+"pageIdFromName.cdb", testPages)
        pageIntValue = CdbDictIntValue(self.dir + "pageIntValue.cdb")

        # test _pack_value and _unpack_value
        expected = 1234
        result = pageIntValue._unpack_value(pageIntValue._pack_value(expected))
        self.assertEqual(result, expected)

        # test _pack_key and _unpack_key
        expected = 'abcde'
        result = pageIntValue._unpack_key(pageIntValue._pack_key(expected))
        self.assertEqual(result, expected)

        pageIntValue.clear()
        pageIntValue.update(testPages)

        self.assertEqual(len(pageIntValue), len(testPages))
        for i in testPages:
            expected = testPages[i]
            result = pageIntValue[i]
            self.assertEqual(result, expected)
        return

        pageIntValue['D'] = 1234
        testPages['D'] = 1234
        self.assertEqual(len(pageIntValue), len(testPages))
        for i in testPages:
            expected = testPages[i]
            result = pageIntValue[i]
            self.assertEqual(result, expected)

        testPages['E'] = 1235
        testPages['F'] = 1236
        pageIntValue.update({'E': 1235, 'F': 1236})
        self.assertEqual(len(pageIntValue), len(testPages))
        for i in testPages:
            print "bb", i
            expected = testPages[i]['id']
            result = pageIntValue[i]
            self.assertEqual(result, expected)

        self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
