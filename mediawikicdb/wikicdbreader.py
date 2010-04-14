#!/bin/env python
#coding=utf-8
#file: wikicdbreader.py

import struct
import cdb


class MediaWikiCdbReader():
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
		importance = t[0] & 0xff
		if importance == 0xff:
			importance = -1
		page['importance'] = importance
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
			importance = t[0] & 0xff
			if importance == 0xff:
				importance = -1
			projects[id] = {'class':cls, 'importance':importance}
		return projects

	def printCdbFromNameFile(self,filename):
		print "\nfile:"+filename
		c = cdb.init(filename)
		k = c.firstkey()
		while k is not None:
			v = c.get(k)
			i = struct.unpack("<l",v)
			print k, "=>", hex(i[0])
			k = c.nextkey()

	def printCdbFromIdFile(self,filename):
		print "\nfile:"+filename
		c = cdb.init(filename)
		k = c.firstkey()
		while k is not None:
			v = c.get(k)
			i = struct.unpack("<l",k)
			print hex(i[0]), "=>", v
			k = c.nextkey()

