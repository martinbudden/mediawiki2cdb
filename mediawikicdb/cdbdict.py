#!/bin/env python
#coding=utf-8
#file: mediawikicdb.py

import struct
import cdb
import os
from ctypes import create_string_buffer


class CdbDict_iter:
    """Iterator for a CDB dictionary."""

    def __init__(self, cdb):
        self.cdb = cdb
        self.key = self.cdb.firstkey()

    def __iter__(self):
        return self

    def next(self):
        if self.key is None:
            raise StopIteration
        key = self.key
        self.key = self.cdb.nextkey()
        return key


class CdbDict(dict):
    """Base class for a dictionary over a CDB file."""

    def __init__(self, filename):
        self.filename = filename
        self.struct = struct.Struct("<l")
        if not os.path.exists(self.filename):
            open(filename, "w").close()
        self.cdb = cdb.init(filename)
        dict.__init__(self)

    def __iter__(self):
        return CdbDict_iter(self.cdb)

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
        return key

    def _unpack_key(self, key):
        return key

    def _pack_value(self, value):
        return value

    def _unpack_value(self, value):
        return value

    def clear(self):
        os.remove(self.filename)
        open(self.filename, "w").close()
        maker = cdb.cdbmake(self.filename, self.filename + ".tmp")
        maker.finish()
        del(maker)
        self.cdb = cdb.init(self.filename)

    def update(self, values):
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
        return self.cdb.keys()


class CdbDictIntKey_iter(CdbDict_iter):
    """Iterator for a CDB dictionary with a 32 bit integer key"""

    def __init__(self, cdb):
        self.struct = struct.Struct("<l")
        CdbDict_iter.__init__(self, cdb)
        #super(CdbDict2_iter, self).__init__(cdb)

    def next(self):
        return self.struct.unpack(CdbDict_iter.next(self))[0]


class CdbDictIntKey(CdbDict):
    """Dictionary over a CDB file, keys are 32 bit integers."""

    def __iter__(self):
        return CdbDictIntKey_iter(self.cdb)

    def __getitem__(self, key):
        # name from id
        return self.cdb.get(self.struct.pack(key))

    def _pack_key(self, key):
        return self.struct.pack(key)

    def _unpack_key(self, key):
        return self.struct.unpack(key)[0]

    def keys(self):
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
        return self.struct.pack(value)

    def _unpack_value(self, value):
        return self.struct.unpack(value)[0]

    def __getitem__(self, key):
        return self.struct.unpack(self.cdb.get(key))[0]
