#!/bin/env python
#coding=utf-8
#file: mediawikicdb.py

"""
CDB dictionary over MediaWiki pages.
"""

import struct
from ctypes import create_string_buffer
from cdbdict import CdbDict, CdbDictIntKey


class CdbDictIdFromName(CdbDict):
    """
    Dictionary over a CDB file, keys are strings,
    values are named 32 bit integers.
    """

    def __getitem__(self, key):
        return {'id': self.struct.unpack(self.cdb.get(key))[0]}

    def _pack_value(self, value):
        """Pack the value's id into a 32-bit little endian integer."""
        return self.struct.pack(value['id'])

    def _unpack_value(self, value):
        """Unpack the value into an id item."""
        return {'id': self.struct.unpack(value)[0]}


class CdbDictNameFromId(CdbDictIntKey):
    """
    Dictionary over a CDB file: keys are 32 bit integers,
    values are named strings
    """

    def __getitem__(self, key):
        #v = self.cdb.get(self.struct.pack(key))
        v = CdbDictIntKey.__getitem__(self, key)
        return self._unpack_value(v)

    def _pack_value(self, v):
        """Pack the value's name."""
        return v['name']

    def _unpack_value(self, v):
        """Unpack the value into a name item."""
        return {'name': v}


class CdbDictPageLinksFromId(CdbDictIntKey):
    """
    Dictionary over a CDB file: keys are 32 bit integers,
    values are pagelinks.
    """

    def __getitem__(self, key):
        #v = self.cdb.get(self.struct.pack(key))
        v = CdbDictIntKey.__getitem__(self, key)
        return self._unpack_value(v)

    def _unpack_value(self, v):
        """Unpack the buffer into class, importance and links items."""
        page = {}

        t = self.struct.unpack(v[0:4])[0]
        offset = 4
        page['class'] = t >> 8
        importance = t & 0xff
        if importance == 0xff:
            importance = -1
        page['importance'] = importance

        page_links = set()
        count = len(v) / 4 - 1
        while count > 0:
            count -= 1
            t = self.struct.unpack(v[offset:offset + 4])[0]
            offset += 4
            page_links.add(long(t))
        page['links'] = page_links
        return page

    def _pack_value(self, v):
        """Pack the value's importance, class and links into a buffer."""
        link_ids = v['links']
        buf = create_string_buffer(4 + len(link_ids) * 4)
        offset = 0
        importance = v['importance']
        if importance == -1:
            importance = 0xff
        struct.pack_into("<l", buf, offset, (v['class'] << 8) | importance)
        offset += 4
        for j in link_ids:
            struct.pack_into("<l", buf, offset, j)
            offset += 4
        return buf


class CdbDictPageProjectsFromId(CdbDictIntKey):
    """
    Dictionary over a CDB file: keys are 32 bit integers,
    values are page projects.
    """

    def _unpack_value(self, v):
        """Unpack the buffer into class, importance and projects items."""
        page = {}
        t = self.struct.unpack(v[0:4])[0]
        offset = 4
        page['class'] = t >> 8
        importance = t & 0xff
        if importance == 0xff:
            importance = -1
        page['importance'] = importance

        projects = {}
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
        page['projects'] = projects
        return page

    def _pack_value(self, v):
        """Pack the value's importance, class and links into a buffer."""
        projects = v['projects']
        buf = create_string_buffer(4 + len(projects) * 4 * 2)
        offset = 0
        importance = v['importance']
        if importance == -1:
            importance = 0xff
        struct.pack_into("<l", buf, offset, (v['class'] << 8) | importance)
        offset += 4
        for j in projects:
            struct.pack_into("<l", buf, offset, j)
            offset += 4
            importance = projects[j]['importance']
            if importance == -1:
                importance = 0xff
            struct.pack_into("<l", buf, offset, (projects[j]['class'] << 8) | importance)
            offset += 4
        return buf


class CdbDictPageFromId(CdbDictIntKey):
    """
    Dictionary over a CDB file: keys are 32 bit integers,
    values are pages.
    """

    def __getitem__(self, key):
        v = self.cdb.get(self.struct.pack(key))
        return self._unpack_value(v)

    def _unpack_value(self, v):
        """
        Unpack the buffer into class, importance, links, projects and name.
        """
        page = {}
        offset = 0
        links_len = long(self.struct.unpack(v[offset:offset + 4])[0])
        offset += 4
        projects_len = long(self.struct.unpack(v[offset:offset + 4])[0])
        offset += 4

        t = self.struct.unpack(v[offset:offset + 4])[0]
        offset += 4
        page['class'] = t >> 8
        importance = t & 0xff
        if importance == 0xff:
            importance = -1
        page['importance'] = importance

        page_links = set()
        count = links_len
        while count > 0:
            count -= 1
            t = self.struct.unpack(v[offset:offset + 4])[0]
            offset += 4
            page_links.add(long(t))
        page['links'] = page_links

        projects = {}
        count = projects_len
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
        """
        Pack the page's class, importance, links, projects and name into a buffer.
        """
        name = v['name']
        link_ids = v['links']
        projects = v['projects']
        buf = create_string_buffer(8 + (4 + len(link_ids) * 4) +
            (len(projects) * 4 * 2) +
            len(name))
        # pack in the lengths of the links and projects sets
        offset = 0
        struct.pack_into("<l", buf, offset, len(link_ids))
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
        for j in link_ids:
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
