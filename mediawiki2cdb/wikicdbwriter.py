#!/bin/env python
#coding=utf-8
#file: wikicdbwriter.py

import struct
from ctypes import create_string_buffer
import cdb


class WikiCdbWriter():
	def writeCdbNameId(self,filename,dictionary):
		maker = cdb.cdbmake(filename, filename + ".tmp")
		s = struct.Struct("<l")
		for i in dictionary:
			maker.add(i,s.pack(dictionary[i]['id']))
		print "Added %d records to CDB %s (fd %d)" % (maker.numentries, maker.fn, maker.fd)
		maker.finish()
		del(maker)

	def writeCdbIdName(self,filename,dictionary):
		maker = cdb.cdbmake(filename, filename + ".tmp")
		s = struct.Struct("<l")
		for i in dictionary:
			maker.add(s.pack(i),dictionary[i]['name'])
		print "Added %d records to CDB %s (fd %d)" % (maker.numentries, maker.fn, maker.fd)
		maker.finish()
		del(maker)

	def writeCdbPageLinks(self,filename,pageIds):
		maker = cdb.cdbmake(filename, filename + ".tmp")
		s = struct.Struct("<l")
		for i in pageIds:
			linkIds = pageIds[i]['linkIds']
			buf = create_string_buffer(len(linkIds)*4+8)
			offset = 0
			struct.pack_into("<l",buf,offset,(pageIds[i]['class']<<8)|pageIds[i]['importance'])
			offset += 4
			for j in linkIds:
				struct.pack_into("<l",buf,offset,j)
				offset += 4
			maker.add(s.pack(i),buf)
		print "Added %d records to CDB %s (fd %d)" % (maker.numentries, maker.fn, maker.fd)
		maker.finish()
		del(maker)

	def writeCdbPageProjects(self,filename,pageIds):
		maker = cdb.cdbmake(filename, filename + ".tmp")
		s = struct.Struct("<l")
		for i in pageIds:
			projects = pageIds[i]['projects']
			buf = create_string_buffer(len(projects)*4*2+4)
			offset = 0
			#struct.pack_into("<l",buf,offset,len(projects))
			#offset += 4
			for j in projects:
				struct.pack_into("<l",buf,offset,j)
				offset += 4
				struct.pack_into("<l",buf,offset,(projects[j]['class']<<8)|projects[j]['importance'])
				offset += 4
			maker.add(s.pack(i),buf)
		print "Added %d records to CDB %s (fd %d)" % (maker.numentries, maker.fn, maker.fd)
		maker.finish()
		del(maker)

	def writeCdbFiles(self,handler):
		# pages: name,id file
		self.writeCdbNameId("../cdb/pages.cdb",handler.pages)
		# pages: id,name file
		self.writeCdbIdName("../cdb/pageIds.cdb",handler.pageIds)
		self.writeCdbPageLinks("../cdb/pageLinks.cdb",handler.pageIds)
		self.writeCdbPageProjects("../cdb/pageProjects.cdb",handler.pageIds)
		# template: name,id file
		self.writeCdbNameId("../cdb/projects.cdb",handler.templates)
		# template: id,name file
		self.writeCdbIdName("../cdb/projectIds.cdb",handler.templateIds)

