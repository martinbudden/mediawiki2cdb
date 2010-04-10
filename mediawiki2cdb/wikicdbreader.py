#!/bin/env python
#coding=utf-8
#file: wikicdbreader.py

import struct
import cdb


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
        dict.__init__(self)
        self.struct = struct.Struct("<l")
        self.cdb = cdb.init(filename)

    def __iter__(self):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise TypeError("'CdbDict' object does not support item assignment")

    def __delitem__(self, key):
        raise TypeError("'CdbDict' object does not support item assignment")

    def keys(self):
        raise NotImplementedError


class CdbDictIdFromName(CdbDict):
    """Dictionary over a CDB file, values are 32 bit integers keys are strings"""

    def __iter__(self):
        return CdbDict_iter(self.cdb)

    def __getitem__(self, key):
        # id from name
        return self.struct.unpack(self.cdb.get(key))[0]

    def keys(self):
        return self.cdb.keys()


class CdbDictIntKey_iter(CdbDict_iter):
    """Iterator for a CDB dictionary with a 32 bit integer key"""

    def __init__(self,cdb):
        CdbDict_iter.__init__(self,cdb)
        #super(CdbDict2_iter, self).__init__(cdb)
        self.struct = struct.Struct("<l")
    def next(self):
        return self.struct.unpack(CdbDict_iter.next(self))[0]

class CdbDict3_iter:
    def __init__(self,cdb):
        self.struct = struct.Struct("<l")
        self.cdb = cdb
        self.key = self.cdb.firstkey()
    def __iter__(self):
        return self
    def next(self):
        if self.key is None:
            raise StopIteration     # end of iteration
        key = self.key
        self.key = self.cdb.nextkey()
        return self.struct.unpack(key)[0]


class CdbDictNameFromId(CdbDict):
    """Dictionary over a CDB file, values are strings keys are 32 bit integers."""
    def __iter__(self):
        return CdbDictIntKey_iter(self.cdb)

    def __getitem__(self, key):
        # name from id
        return self.cdb.get(self.struct.pack(key))

    def keys(self):
        keys = self.cdb.keys()
        for i in range(0,len(keys)):
#            print "kk",i, keys[i]#,self.struct.unpack(i)[0]
            keys[i] = self.struct.unpack(keys[i])[0]
        return keys


class CdbDictPageLinksFromId(CdbDictNameFromId):
    """Dictionary over a CDB file, values are pagelinks, keys are 32 bit integers."""
    def __getitem__(self, key):
        v = self.cdb.get(self.struct.pack(key))
        t = self.struct.unpack(v[0:4])
        offset = 4
        page = {}
        page['class'] = t[0] >> 8
        imp = t[0] & 0xff
        if imp == 0xff:
            imp = -1
        page['importance'] = imp
        t = self.struct.unpack(v[offset:offset+4])
        offset += 4
        pageLinks = set()
        count = len(v)/4 - 3
        while count > 0:
            count -= 1
            t = self.struct.unpack(v[offset:offset+4])
            offset += 4
            pageLinks.add(long(t[0]))
        page['links'] = pageLinks
        return page


class CdbDictPageProjectsFromId(CdbDictNameFromId):
    """Dictionary over a CDB file, values are page projects, keys are 32 bit integers."""
    def __getitem__(self, key):
        v = self.cdb.get(self.struct.pack(key))
        offset = 0
        projects = {}
        count = (len(v)-4)/8
        while count > 0:
            count -= 1
            t = self.struct.unpack(v[offset:offset+4])
            offset += 4
            id = long(t[0])
            t = self.struct.unpack(v[offset:offset+4])
            offset += 4
            cls = t[0] >> 8
            importance = t[0] & 0xff
            if importance == 0xff:
                importance = -1
            projects[id] = {'class':cls, 'importance':importance}
        return projects





class WikiCdbReader():
	def __init__(self,dir):
		self.struct = struct.Struct("<l")
		self.pageIdFromName = cdb.init(dir+"pageIdFromName.cdb")
		self.pageNameFromId = cdb.init(dir+"pageNameFromId.cdb")
		self.pageLinksFromId = cdb.init(dir+"pageLinksFromId.cdb")
		self.pageProjectsFromId = cdb.init(dir+"pageProjectsFromId.cdb")
		self.projectIdFromName = cdb.init(dir+"projectIdFromName.cdb")
		self.projectNameFromId = cdb.init(dir+"projectNameFromId.cdb")

	def getPageIdFromName(self,pageName):
		i = self.struct.unpack(self.pageIdFromName.get(pageName))
		return i[0]

	def getPageNameFromId(self,pageId):
		return self.pageNameFromId.get(self.struct.pack(pageId))

	def getProjectIdFromName(self,projectName):
		i = self.struct.unpack(self.projectIdFromName.get(projectName))
		return i[0]

	def getProjectNameFromId(self,projectId):
		return self.projectNameFromId.get(self.struct.pack(projectId))

	def getPageLinksFromId(self,pageId):
		v = self.pageLinksFromId.get(self.struct.pack(pageId))
		t = self.struct.unpack(v[0:4])
		offset = 4
		page = {}
		page['class'] = t[0] >> 8
		imp = t[0] & 0xff
		if imp == 0xff:
			imp = -1
		page['importance'] = imp
		t = self.struct.unpack(v[offset:offset+4])
		offset += 4
		pageLinks = set()
		count = len(v)/4 - 3
		while count > 0:
			count -= 1
			t = self.struct.unpack(v[offset:offset+4])
			offset += 4
			pageLinks.add(long(t[0]))
		page['links'] = pageLinks
		return page

	def getPageProjectsFromId(self,pageId):
		v = self.pageProjectsFromId.get(self.struct.pack(pageId))
		offset = 0
		projects = {}
		count = (len(v)-4)/8
		while count > 0:
			count -= 1
			t = self.struct.unpack(v[offset:offset+4])
			offset += 4
			id = long(t[0])
			t = self.struct.unpack(v[offset:offset+4])
			offset += 4
			cls = t[0] >> 8
			imp = t[0] & 0xff
			if imp == 0xff:
				imp = -1
			projects[id] = {'class':cls, 'importance':imp}
		return projects

	def printCdbFile(self,filename):
		print "\nfile:"+filename
		c = cdb.init(filename)
		k = c.firstkey()
		while k is not None:
			v = c.get(k)
			i = struct.unpack("<l",v)
			print k, "=>", hex(i[0])
			k = c.nextkey()

	def printCdbIdFile(self,filename):
		print "\nfile:"+filename
		c = cdb.init(filename)
		k = c.firstkey()
		while k is not None:
			v = c.get(k)
			i = struct.unpack("<l",k)
			print hex(i[0]), "=>", v
			k = c.nextkey()

