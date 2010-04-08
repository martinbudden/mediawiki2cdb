#!/bin/env python
#coding=utf-8
#file: wikicdbreader.py

import struct
import cdb


class WikiCdbReader():
	def __init__(self):
		self.struct = struct.Struct("<l")
		self.pages = cdb.init("../cdb/pages.cdb")
		self.pageIds = cdb.init("../cdb/pageIds.cdb")
		self.pageLinks = cdb.init("../cdb/pageLinks.cdb")
		self.pageProjects = cdb.init("../cdb/pageProjects.cdb")
		self.projects = cdb.init("../cdb/projects.cdb")
		self.projectIds = cdb.init("../cdb/projectIds.cdb")

	def getPageId(self,pageName):
		i = self.struct.unpack(self.pages.get(pageName))
		return i[0]

	def getPageName(self,pageId):
		return self.pageIds.get(self.struct.pack(pageId))

	def getProjectId(self,projectName):
		i = self.struct.unpack(self.projects.get(projectName))
		return i[0]

	def getProjectName(self,projectId):
		return self.projectIds.get(self.struct.pack(projectId))

	def getPageLinks(self,pageId):
		v = self.pageLinks.get(self.struct.pack(pageId))
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

	def getPageProjects(self,pageId):
		v = self.pageProjects.get(self.struct.pack(pageId))
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

