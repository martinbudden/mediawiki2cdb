#!/bin/env python
#coding=utf-8
# file: mediawikixmltocdb.py

#!!! need to deal with normalization of link titles

from xml.sax import make_parser, SAXException
import xml.sax.handler
import re
import sys
import time

class WikiHandler(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.stack = []
		self.elementIndex =0
		self.limit = 100000
		self.dispCount = 0
		self.count = 0
		self.inElement = ""
		self.id = 0
		self.nextId = long(-1)
		self.title = ""
		self.text = ""
		self.pages = {}
		self.pageRedirects = {}
		self.templates = {}
		self.templateRedirects = {}
		self.talkpages = {}

	def startElement(self, name, attributes):
		self.elementIndex += 1
		if self.elementIndex > self.limit and self.limit > 0:
			raise SAXException('Reached limit count') # stop parsing
		self.stack.append(name)
		self.inElement = name
		if name == "page":
			self.title = ""
			self.id = 0
			self.text = ""

	def characters(self, data):
		if self.inElement == "title" and self.title == "":
			self.title = data.encode("utf-8")
			self.dispCount += 1
			self.count += 1
			if self.dispCount==100:
				self.dispCount = 0
				sys.stderr.write(str(self.count) + ":" + self.title + "\n")
				#print str(self.count) + ":" + self.title
		elif self.inElement == "id" and self.id == 0 and self.stack[len(self.stack)-2] == "page":
			if data.isdigit():
				self.id = long(data)
		elif self.inElement == "text":
			self.text += data

	def endElement(self, name):
		self.stack.pop()
		if name == "page":
			if self.id == 0:
				# article did not have an id, so create one, created ids are negative
				self.id = self.nextId
				self.nextId -= 1
			if self.title.find(":") == -1:
				r = self.text.lstrip()[0:9]
				if r[0] == "#" and r.upper() == "#REDIRECT":
					self.pageRedirects[self.title] = {'id':self.id,'redirect':self.getRedirect(self.text)}
				else:
					self.pages[self.title] = {'id':self.id,'links':self.getPageLinks(self.text)}
			elif self.title.startswith("Template:"):
				title = self.title[9:]
				r = self.text.lstrip()[0:9]
				if r[0] == "#" and r.upper() == "#REDIRECT":
					redirect = self.getRedirect(self.text)
					if redirect.startswith("Template:"):
						redirect = redirect[9:]
					self.templateRedirects[title] = {'id':self.id,'redirect':redirect}
				else:
					self.templates[title] = {'id':self.id}
			elif self.title.startswith("Talk:"):
				self.talkpages[self.title[5:]] = {'id':self.id,'projects':self.getProjects(self.text)}
			elif self.title.startswith("Media:") or\
					self.title.startswith("Special:") or\
					self.title.startswith("User:") or\
					self.title.startswith("User talk:") or\
					self.title.startswith("Wikipedia:") or\
					self.title.startswith("Wikipedia talk:") or\
					self.title.startswith("File:") or\
					self.title.startswith("File talk:") or\
					self.title.startswith("MediaWiki:") or\
					self.title.startswith("MediaWiki talk:") or\
					self.title.startswith("Template talk:") or\
					self.title.startswith("Help:") or\
					self.title.startswith("Help talk:") or\
					self.title.startswith("Category:") or\
					self.title.startswith("Category talk:") or\
					self.title.startswith("Portal:") or\
					self.title.startswith("Portal talk:"):
				pass #x = "" # do nothing
			else:
				r = self.text.lstrip()[0:9]
				if r[0] == "#" and r.upper() == "#REDIRECT":
					self.pageRedirects[self.title] = {'id':self.id,'redirect':self.getRedirect(self.text)}
				else:
					self.pages[self.title] = {'id':self.id,'links':self.getPageLinks(self.text)}

	def getRedirect(self,text):
		redirect = ""
		r = re.compile(r"\[\[([^#\[\]]*)")
		m = r.search(text)
		if m:
			redirect = m.group(1)
		return redirect

	def getProjects(self,text):
		classes = {'fa':7,'ga':6,'a':5,'b':4,'c':3,'start':2,'stub':1,'list':0,'':-1}
		imps = {'top':3,'high':2,'mid':1,'low':0,'':-1}
		projects = {}
		t = re.compile(r"{{([^{}]*)}}")
		i = re.compile(r"importance=(\w*)")
		c = re.compile(r"class=(\w*)")
		for match in t.finditer(text):
			template = match.group(1)
			# if the template contains either a class or an importance parameter, then assume it is a project template
			if template.find("class=")!=-1 or template.find("importance=")!=-1:
				importance = -1
				m = i.search(template)
				if m:
					name = m.group(1).lower().encode("utf-8")
					val = imps.get(name)
					if val:
						importance = val
				cls = -1
				m = c.search(template)
				if m:
					name = m.group(1).lower().encode("utf-8")
					val = classes.get(name)
					if val:
						cls = val
				pos = template.find("|")
				if pos!=-1:
					template = template[0:pos].strip()
					if template.startswith("Template:"):
						template = template[9:]
					projects[template] = {'class':cls,'importance':importance}
		return projects

	def getPageLinks(self,text):
		pagelinks = set()
		p = re.compile(r"\[\[([^\[\]\:]*)\]\]")
		for match in p.finditer(text):
			link = match.group(1)
			pos = link.find("|")
			if pos!=-1:
				link = link[0:pos]
			pos = link.find("#")
			if len(link) > 0 and pos != 0: # '#' in pos 0 is link to section in same page, so do not add to pagelinks
				if pos!=-1:
					link = link[0:pos]
				link = link[0].upper() + link[1:].replace('_',' ') if len(link) > 1 else link[0].upper()
				pagelinks.add(link)
		return pagelinks


class WikiInfo():
	def __init__(self):
		self.pages = {}
		self.pageRedirects = {}
		self.templates = {}
		self.templateRedirects = {}
		self.talkpages = {}
		# derived dictionaries
		self.pageIds = {}
		self.templateIds = {}

	def set(self,handler):
		self.pages = handler.pages
		self.pageRedirects = handler.pageRedirects
		self.templates = handler.templates
		self.templateRedirects = handler.templateRedirects
		self.talkpages = handler.talkpages
	def doStuff(self):
		self.setTemplateIds()
		self.replaceRedirects()
		self.setPageLinkIds()
		self.setPageProjectIds()

	def replaceTemplateRedirects(self):
		# go through the templates of every talk page, replacing redirected template names with the primary template name
		for i in self.talkpages:
			projects = {}
			p = self.talkpages[i]['projects']
			for j in p:
				name = j
				while name in self.templateRedirects:
					name = self.templateRedirects[name]['redirect']
				projects[name] = p[j]
			self.talkpages[i]['projects'] = projects

	def replacePageRedirects(self):
		# go through the links of every page, replacing redirected page names with the primary page name
		for i in self.pages:
			links = set()
			p = self.pages[i]['links']
			for j in p:
				name = j
				while name in self.pageRedirects:
					name = self.pageRedirects[name]['redirect']
				links.add(name)
			#pagelinks.sort()
			self.pages[i]['links'] = links

	def setPageLinkIds(self):
		print "setPageLinkIds"
		for i in self.pages:
			linkIds = set()
			links = self.pages[i]['links']
			for j in links:
				if j in self.pages:
					linkId = self.pages[j]['id']
					linkIds.add(linkId)
				else:
					linkId = j
					normalizedJ = j[0].upper() + j[1:].replace('_',' ') if len(j) > 1 else j[0].upper()
					if normalizedJ in self.pages:
						linkId = self.pages[normalizedJ]['id']
						linkIds.add(linkId)
				#linkIds.add(linkId)
			self.pageIds[self.pages[i]['id']] = {'name':i,'linkIds':linkIds}

	def setPageProjectIds(self):
		print "setProjectIds"
		for i in self.pageIds:
			name = self.pageIds[i]['name']
			projectIds = {}
			try:
				projects = self.talkpages[name]['projects']
			except:
				projects = {}
			cls = -1
			imp = -1
			for j in projects:
				id = None
				if j in self.templates:
					id = self.templates[j]['id']
				else:
					normalizedJ = j[0].upper() + j[1:].replace('_',' ') if len(j) > 1 else j[0].upper()
					if normalizedJ in self.templates:
						id = self.templates[normalizedJ]['id']
				p = projects[j]
				if id:
					projectIds[id] = p
				#else:
				#	print "no template for project:"+j
				if p['class'] > cls:
					cls = p['class']
				if p['importance'] > imp:
					imp = p['importance']
			self.pageIds[i]['projects'] = projectIds
			self.pageIds[i]['importance'] = imp
			self.pageIds[i]['class'] = cls

	def setTemplateIds(self):
		print "setTemplateIds"
		for i in self.templates:
			self.templateIds[self.templates[i]['id']] = {'name':i}

	def replaceRedirects(self):
		self.replaceTemplateRedirects()
		self.replacePageRedirects()


def parseMediaWikiXMLExport(filename):
	"""
	produces 5 hash tables: pages,pageRedirects,templates,templateRedirects,talkPages
	self.pages[title] = {'id':self.id,'links':getPageLinks(self.text)}
	self.pageRedirects[title] = {'id':self.id,'redirect':getRedirect(self.text)}
	self.talkpages[title] = {'id':self.id,'projects':getProjects(self.text)}
	self.templates[title] = {'id':self.id}
	self.templateRedirects[title] = {'id':self.id,'redirect':redirect}
	"""
	handler = WikiHandler()
	parser = xml.sax.make_parser()
	parser.setContentHandler(handler)
	try:
		parser.parse(filename)
	except SAXException:
		print "caught"
	return handler


def parseXmlFile(fileName):
	t0 = time.time()
	handler = parseMediaWikiXMLExport(fileName)
	t1 = time.time()
	print "Time1:",t1 - t0
	sys.stderr.write("Time:" + str(t1 - t0) + "\n")

	info = WikiInfo()
	info.set(handler)
	info.doStuff()

	
	t2 = time.time()
	print "Time2:",t2 - t1
	sys.stderr.write("Time:" + str(t2 - t1) + "\n")
	return info


