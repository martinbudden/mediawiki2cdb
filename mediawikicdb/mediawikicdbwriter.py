#!/bin/env python
#coding=utf-8
#file: mediawikicdbwriter.py

import struct
from ctypes import create_string_buffer
import cdb


class MediaWikiCdbWriter():
	def writeCdbIdFromName(self,filename,dictionary):
		maker = cdb.cdbmake(filename, filename + ".tmp")
		s = struct.Struct("<l")
		for i in dictionary:
			maker.add(i,s.pack(dictionary[i]['id']))
		print "Added %d records to CDB %s (fd %d)" % (maker.numentries, maker.fn, maker.fd)
		maker.finish()
		del(maker)

	def writeCdbNameFromId(self,filename,dictionary):
		maker = cdb.cdbmake(filename, filename + ".tmp")
		s = struct.Struct("<l")
		for i in dictionary:
			maker.add(s.pack(i),dictionary[i]['name'])
		print "Added %d records to CDB %s (fd %d)" % (maker.numentries, maker.fn, maker.fd)
		maker.finish()
		del(maker)

	def writeCdbPageLinks(self,filename,pageFromId):
		maker = cdb.cdbmake(filename, filename + ".tmp")
		s = struct.Struct("<l")
		for i in pageFromId:
			linkIds = pageFromId[i]['linkIds']
			buf = create_string_buffer(len(linkIds)*4+8)
			offset = 0
			struct.pack_into("<l",buf,offset,(pageFromId[i]['class']<<8)|pageFromId[i]['importance'])
			offset += 4
			for j in linkIds:
				struct.pack_into("<l",buf,offset,j)
				offset += 4
			maker.add(s.pack(i),buf)
		print "Added %d records to CDB %s (fd %d)" % (maker.numentries, maker.fn, maker.fd)
		maker.finish()
		del(maker)

	def writeCdbPageProjects(self,filename,pageFromId):
		maker = cdb.cdbmake(filename, filename + ".tmp")
		s = struct.Struct("<l")
		for i in pageFromId:
			projects = pageFromId[i]['projects']
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

	def writeCdbFiles(self,info,cdbdir):
		# pages: name,id file
		self.writeCdbIdFromName(cdbdir+"pageIdFromName.cdb",info.pages)
		# pages: id,name file
		self.writeCdbNameFromId(cdbdir+"pageNameFromId.cdb",info.pageFromId)
		self.writeCdbPageLinks(cdbdir+"pageLinksFromId.cdb",info.pageFromId)
		self.writeCdbPageProjects(cdbdir+"pageProjectsFromId.cdb",info.pageFromId)
		# template: name,id file
		self.writeCdbIdFromName(cdbdir+"projectIdFromName.cdb",info.templates)
		# template: id,name file
		self.writeCdbNameFromId(cdbdir+"projectNameFromId.cdb",info.templateFromId)

