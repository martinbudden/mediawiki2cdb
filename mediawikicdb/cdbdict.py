#!/bin/env python
#coding=utf-8
#file: mediawikicdb.py

import struct
import cdb
import os


class CdbDictIter:
    """Iterator for a CDB dictionary."""

    def __init__(self, cdb):
        self.cdb = cdb
        self.key = self.cdb.firstkey()

    def __iter__(self):
        return self

    def next(self):
        """Return the next key for the iterator."""
        if self.key is None:
            raise StopIteration
        key = self.key
        self.key = self.cdb.nextkey()
        return key


class CdbDict(dict):
    """Base class for a dictionary over a CDB file."""

    def __init__(self, filename):
        self.filename = filename
        self.struct = struct.Struct("<l")  # "<l" is 32bit little endian integer
        if not os.path.exists(self.filename):
            open(filename, "w").close()
        self.cdb = cdb.init(filename)
        dict.__init__(self)

    def __iter__(self):
        return CdbDictIter(self.cdb)

    def __setitem__(self, key, value):
        raise TypeError("'CdbDict' object does not support item setting")
        #maker = cdb.cdbmake(self.filename, self.filename + ".tmp")
        #maker.add(self._pack_key(key),self._pack_value(value))
        #maker.finish()
        #del(maker)
        #self.cdb = cdb.init(self.filename)

    def __getitem__(self, key):
        return self._unpack_value(self.cdb.get(self._pack_key(key)))

    def __delitem__(self, key):
        raise TypeError("'CdbDict' object does not support item deletion")

    def __len__(self):
        return len(self.cdb.keys())

    def _pack_key(self, key):
        """
        Method to allow subclasses to change how the key is packed. By default leave key unchanged.
        """
        return key

    def _unpack_key(self, key):
        """
        Method to unpack key, must complement _pack_key.
        """
        return key

    def _pack_value(self, value):
        """
        Method to allow subclasses to change how the value is packed. By default leave value unchanged.
        """
        return value

    def _unpack_value(self, value):
        """
        Method to unpack value, must complement _pack_value.
        """
        return value

    def clear(self):
        """Remove all entries from the dictionary."""
        os.remove(self.filename)
        open(self.filename, "w").close()
        maker = cdb.cdbmake(self.filename, self.filename + ".tmp")
        maker.finish()
        del(maker)
        self.cdb = cdb.init(self.filename)

    def update(self, values):
        """Add values to the dictionary."""
        maker = cdb.cdbmake(self.filename, self.filename + ".tmp")
        for i in values:
            # add key,value
            maker.add(self._pack_key(i), self._pack_value(values[i]))
        print "Added %d records to CDB %s (fd %d)" \
            % (maker.numentries, maker.fn, maker.fd)
        maker.finish()
        del(maker)
        self.cdb = cdb.init(self.filename)

    def keys(self):
        """Return a list of the dictionary keys."""
        return self.cdb.keys()


class CdbDictIntKeyIter(CdbDictIter):
    """Iterator for a CDB dictionary with a 32 bit integer key"""

    def __init__(self, cdb):
        self.struct = struct.Struct("<l")
        CdbDictIter.__init__(self, cdb)
        #super(CdbDictIter, self).__init__(cdb)

    def next(self):
        """Return the next key for the iterator."""
        return self.struct.unpack(CdbDictIter.next(self))[0]


class CdbDictIntKey(CdbDict):
    """Dictionary over a CDB file, keys are 32 bit integers."""

    def __iter__(self):
        return CdbDictIntKeyIter(self.cdb)

    def __getitem__(self, key):
        # name from id
        return self.cdb.get(self.struct.pack(key))

    def _pack_key(self, key):
        """Pack key into a 32-bit little endian integer."""
        return self.struct.pack(key)

    def _unpack_key(self, key):
        """Unpack key from a 32-bit little endian integer."""
        return self.struct.unpack(key)[0]

    def keys(self):
        """Return a list of the dictionary keys."""
        # very primitive implementation
        keys = self.cdb.keys()
        for i in range(0, len(keys)):
            keys[i] = self.struct.unpack(keys[i])[0]
        return keys


class CdbDictIntValue(CdbDict):
    """
    Dictionary over a CDB file, values are 32 bit integers keys are strings
    """

    def _pack_value(self, value):
        """Pack value into a 32-bit little endian integer."""
        return self.struct.pack(value)

    def _unpack_value(self, value):
        """Unpack value from a 32-bit little endian integer."""
        return self.struct.unpack(value)[0]

    def __getitem__(self, key):
        """
        Replacing base function is a performance optimisation and is strictly unnecessary.
        """
        return self.struct.unpack(self.cdb.get(key))[0]
