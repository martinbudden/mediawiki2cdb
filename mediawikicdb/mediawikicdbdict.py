#!/bin/env python
#coding=utf-8
#file: mediawikicdb.py

import struct
import cdb
import os


class CdbDict_iter:
    """Iterator for a CDB dictionary."""

    def __init__(self,cdb):
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
            open(filename,"w").close()
        self.cdb = cdb.init(filename)
        dict.__init__(self)

    def __iter__(self):
        return CdbDict_iter(self.cdb)

    def __setitem__(self, key, value):
        maker = cdb.cdbmake(self.filename, self.filename + ".tmp")
        maker.add(self._pack_key(key),self._pack_value(value))
        maker.finish()
        del(maker)
        self.cdb = cdb.init(self.filename)

    def __getitem__(self, key):
        return self._unpack_value(self._pack_key(key))

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
        open(self.filename,"w").close()
        maker = cdb.cdbmake(self.filename, self.filename + ".tmp")
        maker.finish()
        del(maker)
        self.cdb = cdb.init(self.filename)

    def update(self,values):
        if not os.path.exists(self.filename):
            open(self.filename,"w").close()
        maker = cdb.cdbmake(self.filename, self.filename + ".tmp")
        for i in values:
            # add key,value
            maker.add(self._pack_key(i),self._pack_value(values[i]))
        print "Added %d records to CDB %s (fd %d)" % (maker.numentries, maker.fn, maker.fd)
        maker.finish()
        del(maker)
        self.cdb = cdb.init(self.filename)

    def keys(self):
        return self.cdb.keys()


class CdbDictIntKey_iter(CdbDict_iter):
    """Iterator for a CDB dictionary with a 32 bit integer key"""

    def __init__(self,cdb):
        self.struct = struct.Struct("<l")
        CdbDict_iter.__init__(self,cdb)
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
        for i in range(0,len(keys)):
            keys[i] = self.struct.unpack(keys[i])[0]
        return keys


class CdbDictIntValue(CdbDict):
    """Dictionary over a CDB file, values are 32 bit integers keys are strings"""

    def _pack_value(self, value):
        return self.struct.pack(value)

    def _unpack_value(self, value):
        return self.struct.unpack(value)[0]

    def __getitem__(self, key):
        return self.struct.unpack(self.cdb.get(key))[0]





class CdbDictIdFromName(CdbDict):
    """Dictionary over a CDB file, values are 32 bit integers keys are strings"""

    def _pack_value(self, value):
        return self.struct.pack(value['id'])

    def _unpack_value(self, value):
        return {'id':self.struct.unpack(value)[0]}

    def __getitem__(self, key):
        return {'id':self.struct.unpack(self.cdb.get(key))[0]}


class CdbDictNameFromId(CdbDictIntKey):
    """Dictionary over a CDB file, values are strings keys are 32 bit integers."""

    def __getitem__(self, key):
        #v = self.cdb.get(self.struct.pack(key))
        v = CdbDictIntKey.__getitem__(self,key)
        return self._unpack_value(v)

    def _pack_value(self, v):
        return v['name']

    def _unpack_value(self, v):
        return {'name':v}


class CdbDictPageLinksFromId(CdbDictIntKey):
    """Dictionary over a CDB file, values are pagelinks, keys are 32 bit integers."""

    def __getitem__(self, key):
        #v = self.cdb.get(self.struct.pack(key))
        v = CdbDictIntKey.__getitem__(self,key)
        return self._unpack_value(v)

    def _unpack_value(self, v):
        page = {}

        t = self.struct.unpack(v[0:4])[0]
        offset = 4
        page['class'] = t >> 8
        importance = t & 0xff
        if importance == 0xff:
            importance = -1
        page['importance'] = importance

        pageLinks = set()
        count = len(v)/4 - 2
        while count > 0:
            count -= 1
            t = self.struct.unpack(v[offset:offset+4])[0]
            offset += 4
            pageLinks.add(long(t))
        page['links'] = pageLinks
        return page


class CdbDictPageProjectsFromId(CdbDictIntKey):
    """Dictionary over a CDB file, values are page projects, keys are 32 bit integers."""

#    def __getitem__(self, key):

    def _unpack_value(self, v):
        #v = self.cdb.get(self.struct.pack(key))
        projects = {}
        offset = 0
        count = (len(v)-4)/8
        while count > 0:
            count -= 1
            t = self.struct.unpack(v[offset:offset+4])[0]
            offset += 4
            id = long(t)
            t = self.struct.unpack(v[offset:offset+4])[0]
            offset += 4
            cls = t >> 8
            importance = t & 0xff
            if importance == 0xff:
                importance = -1
            projects[id] = {'class':cls, 'importance':importance}
        return projects

    def _pack_value(self, v):
        linkIds = v['links']
        buf = create_string_buffer(4+len(linkIds)*4)
        offset = 0
        struct.pack_into("<l",buf,offset,(v['class']<<8)|v['importance'])
        offset += 4
        for j in linkIds:
            struct.pack_into("<l",buf,offset,j)
            offset += 4
        return buf


class CdbDictPageFromId(CdbDictNameFromId):
	"""Dictionary over a CDB file, values are page projects, keys are 32 bit integers."""

	def __getitem__(self, key):
		page = {}

		v = self.cdb.get(self.struct.pack(key))
		offset = 0
		linksLen = long(self.struct.unpack(v[offset:offset+4])[0])
		offset += 4
		projectsLen = long(self.struct.unpack(v[offset:offset+4])[0])
		offset += 4

		t = self.struct.unpack(v[offset:offset+4])[0]
		offset += 4
		page['class'] = t >> 8
		importance = t & 0xff
		if importance == 0xff:
			importance = -1
		page['importance'] = importance

		pageLinks = set()
		count = linksLen
		while count > 0:
			count -= 1
			t = self.struct.unpack(v[offset:offset+4])[0]
			offset += 4
			pageLinks.add(long(t))
		page['links'] = pageLinks

		projects = {}
		count = projectsLen
		while count > 0:
			count -= 1
			t = self.struct.unpack(v[offset:offset+4])[0]
			offset += 4
			id = long(t)
			t = self.struct.unpack(v[offset:offset+4])[0]
			offset += 4
			cls = t >> 8
			importance = t & 0xff
			if importance == 0xff:
				importance = -1
			projects[id] = {'class':cls, 'importance':importance}
		page['projects'] = projects
		page['name'] = v[offset:]

		return page


