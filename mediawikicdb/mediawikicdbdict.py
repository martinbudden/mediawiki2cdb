#!/bin/env python
#coding=utf-8
#file: mediawikicdb.py

import struct
import cdb
import os
from ctypes import create_string_buffer
from cdbdict import CdbDict, CdbDictIntKey, CdbDictIntValue


class CdbDictIdFromName(CdbDict):
    """Dictionary over a CDB file, values are 32 bit integers keys are strings"""

    def _pack_value(self, value):
        return self.struct.pack(value['id'])

    def _unpack_value(self, value):
        return {'id': self.struct.unpack(value)[0]}

    def __getitem__(self, key):
        return {'id': self.struct.unpack(self.cdb.get(key))[0]}


class CdbDictNameFromId(CdbDictIntKey):
    """Dictionary over a CDB file, values are strings keys are 32 bit integers."""

    def __getitem__(self, key):
        #v = self.cdb.get(self.struct.pack(key))
        v = CdbDictIntKey.__getitem__(self, key)
        return self._unpack_value(v)

    def _pack_value(self, v):
        return v['name']

    def _unpack_value(self, v):
        return {'name': v}


class CdbDictPageLinksFromId(CdbDictIntKey):
    """Dictionary over a CDB file, values are pagelinks, keys are 32 bit integers."""

    def __getitem__(self, key):
        #v = self.cdb.get(self.struct.pack(key))
        v = CdbDictIntKey.__getitem__(self, key)
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
        count = len(v) / 4 - 2
        while count > 0:
            count -= 1
            t = self.struct.unpack(v[offset:offset + 4])[0]
            offset += 4
            pageLinks.add(long(t))
        page['links'] = pageLinks
        return page


class CdbDictPageProjectsFromId(CdbDictIntKey):
    """Dictionary over a CDB file, values are page projects, keys are 32 bit integers."""

    def _unpack_value(self, v):
        #v = self.cdb.get(self.struct.pack(key))
        projects = {}
        offset = 0
        count = (len(v) - 4) / 8
        while count > 0:
            count -= 1
            t = self.struct.unpack(v[offset:offset + 4])[0]
            offset += 4
            ident = long(t)
            t = self.struct.unpack(v[offset:offset + 4])[0]
            offset += 4
            cls = t >> 8
            importance = t & 0xff
            if importance == 0xff:
                importance = -1
            projects[ident] = {'class': cls, 'importance': importance}
        return projects

    def _pack_value(self, v):
        linkIds = v['links']
        buf = create_string_buffer(4 + len(linkIds) * 4)
        offset = 0
        struct.pack_into("<l", buf, offset, (v['class'] << 8) | v['importance'])
        offset += 4
        for j in linkIds:
            struct.pack_into("<l", buf, offset, j)
            offset += 4
        return buf


class CdbDictPageFromId(CdbDictIntKey):
	"""Dictionary over a CDB file, values are page projects, keys are 32 bit integers."""

	def __getitem__(self, key):
		v = self.cdb.get(self.struct.pack(key))
		return self._unpack_value(v)

	def _unpack_value(self, v):
		page = {}
		offset = 0
		linksLen = long(self.struct.unpack(v[offset:offset + 4])[0])
		offset += 4
		projectsLen = long(self.struct.unpack(v[offset:offset + 4])[0])
		offset += 4

		t = self.struct.unpack(v[offset:offset + 4])[0]
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
			t = self.struct.unpack(v[offset:offset + 4])[0]
			offset += 4
			pageLinks.add(long(t))
		page['links'] = pageLinks

		projects = {}
		count = projectsLen
		while count > 0:
			count -= 1
			t = self.struct.unpack(v[offset:offset + 4])[0]
			offset += 4
			ident = long(t)
			t = self.struct.unpack(v[offset:offset + 4])[0]
			offset += 4
			cls = t >> 8
			importance = t & 0xff
			if importance == 0xff:
				importance = -1
			projects[ident] = {'class': cls, 'importance': importance}
		page['projects'] = projects
		page['name'] = v[offset:]
		return page

	def _pack_value(self, v):
		name = v['name']
		linkIds = v['links']
		projects = v['projects']
		buf = create_string_buffer(8 + (4 + len(linkIds) * 4) + (len(projects) * 4 * 2) + len(name))
		# pack in the lengths of the links and projects sets
		offset = 0
		struct.pack_into("<l", buf, offset, len(linkIds))
		offset += 4
		struct.pack_into("<l", buf, offset, len(projects))
		offset += 4
		# pack in the page class and importance
		importance = v['importance']
		if importance == -1:
			importance = 0xff
		struct.pack_into("<l", buf, offset, (v['class'] << 8) | importance)
		offset += 4
		# pack in the links
		for j in linkIds:
			struct.pack_into("<l", buf, offset, j)
			offset += 4
		# pack in the projects
		for j in projects:
			struct.pack_into("<l", buf, offset, j)
			offset += 4
			importance = projects[j]['importance']
			if importance == -1:
				importance = 0xff
			struct.pack_into("<l", buf, offset, (projects[j]['class'] << 8) | importance)
			offset += 4
		# pack in the name
		buf[offset:] = name
		return buf
