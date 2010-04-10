"""
MediaWiki Info class
"""

#!!! need to deal with normalization of link titles


class WikiInfo():
	def __init__(self):
		self.pages = {}
		self.pageRedirects = {}
		self.templates = {}
		self.templateRedirects = {}
		self.talkpages = {}
		# derived dictionaries
		self.pageFromId = {}
		self.templateFromId = {}

	def set(self,pages,pageRedirects,templates,templateRedirects,talkpages):
		self.pages = pages
		self.pageRedirects = pageRedirects
		self.templates = templates
		self.templateRedirects = templateRedirects
		self.talkpages = talkpages

	def doStuff(self):
		self.setTemplateFromId()
		self.replaceTemplateRedirects()
		self.replacePageRedirects()
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
			self.pageFromId[self.pages[i]['id']] = {'name':i,'linkIds':linkIds}

	def setPageProjectIds(self):
		print "setProjectIds"
		for i in self.pageFromId:
			name = self.pageFromId[i]['name']
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
			self.pageFromId[i]['projects'] = projectIds
			self.pageFromId[i]['importance'] = imp
			self.pageFromId[i]['class'] = cls

	def setTemplateFromId(self):
		print "setTemplateIds"
		for i in self.templates:
			self.templateFromId[self.templates[i]['id']] = {'name':i}

