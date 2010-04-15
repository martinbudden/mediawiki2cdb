#!/bin/env python
#coding=utf-8
# file: mediawikixmlparser.py
"""
MediaWiki XML export parser
"""

#!!! need to deal with normalization of link titles

from xml.sax import make_parser, SAXException
import xml.sax.handler
import re
import sys


class MediaWikiHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self.stack = []
        self.elementIndex = 0
        self.limit = 100000
        self.dispCount = 0
        self.count = 0
        self.inElement = ""
        self.id = 0
        self.nextId = long(-1)
        self.title = ""
        self.text = ""
        self.pages = {}  # pageFromName
        self.pageRedirects = {}
        self.templates = {}  # templateIdFromName
        self.templateRedirects = {}  # templateRedirectFromName
        self.talkpages = {}

    def startElement(self, name, attributes):
        self.elementIndex += 1
        if self.elementIndex > self.limit and self.limit > 0:
            raise SAXException('Reached limit count')  # stop parsing
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
            if self.dispCount == 100:
                self.dispCount = 0
                sys.stderr.write(str(self.count) + ":" + self.title + "\n")
                #print str(self.count) + ":" + self.title
        elif self.inElement == "id" and self.id == 0 and self.stack[len(self.stack) - 2] == "page":
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
                # deal with the most common case, a normal page, first
                r = self.text.lstrip()[0:9]
                if r[0] == "#" and r.upper() == "#REDIRECT":
                    self.pageRedirects[self.title] = {'id': self.id, 'redirect': self.getRedirect(self.text)}
                else:
                    self.pages[self.title] = {'id': self.id, 'links': self.getPageLinks(self.text)}
            elif self.title.startswith("Template:"):
                title = self.title[9:]
                r = self.text.lstrip()[0:9]
                if r[0] == "#" and r.upper() == "#REDIRECT":
                    redirect = self.getRedirect(self.text)
                    if redirect.startswith("Template:"):
                        redirect = redirect[9:]
                    self.templateRedirects[title] = {'id': self.id, 'redirect': redirect}
                else:
                    self.templates[title] = {'id': self.id}
            elif self.title.startswith("Talk:"):
                # the projects a page belongs to are listed in its talk pages
                self.talkpages[self.title[5:]] = {'id': self.id, 'projects': self.getProjects(self.text)}
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
                # ignore any of these namespaces
                pass
            else:
                # the page is not in any namespace, so it must just be a normal page with a ":" in its title
                r = self.text.lstrip()[0:9]
                if r[0] == "#" and r.upper() == "#REDIRECT":
                    self.pageRedirects[self.title] = {'id': self.id, 'redirect': self.getRedirect(self.text)}
                else:
                    self.pages[self.title] = {'id': self.id, 'links': self.getPageLinks(self.text)}

    def getRedirect(self, text):
        redirect = ""
        r = re.compile(r"\[\[([^#\[\]]*)")
        m = r.search(text)
        if m:
            redirect = m.group(1)
        return redirect

    def getProjects(self, text):
        classes = {'fa': 7, 'ga': 6, 'a': 5, 'b': 4, 'c': 3, 'start': 2, 'stub': 1, 'list': 0, '': -1}
        imps = {'top': 3, 'high': 2, 'mid': 1, 'low': 0, '': -1}
        projects = {}
        t = re.compile(r"{{([^{}]*)}}")
        i = re.compile(r"importance=(\w*)")
        c = re.compile(r"class=(\w*)")
        for match in t.finditer(text):
            template = match.group(1)
            if template.find("class=") != -1 or template.find("importance=") != -1:
                # if the template contains either a class or an importance parameter, then assume it is a project template
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
                if pos != -1:
                    template = template[0:pos].strip()
                    if template.startswith("Template:"):
                        template = template[9:]
                    projects[template] = {'class': cls, 'importance': importance}
        return projects

    def getPageLinks(self, text):
        pagelinks = set()
        p = re.compile(r"\[\[([^\[\]\:]*)\]\]")
        for match in p.finditer(text):
            link = match.group(1)
            pos = link.find("|")
            if pos != -1:
                link = link[0:pos]
            pos = link.find("#")
            if len(link) > 0 and pos != 0:  # '#' in pos 0 is link to section in same page, so do not add to pagelinks
                if pos != -1:
                    link = link[0:pos]
                link = link[0].upper() + link[1:].replace('_', ' ') if len(link) > 1 else link[0].upper()
                pagelinks.add(link)
        return pagelinks


def parseMediaWikiXMLExport(filename):
    """
    produces 5 hash tables: pages,pageRedirects,templates,templateRedirects,talkPages
    self.pages[title] = {'id':self.id,'links':getPageLinks(self.text)}
    self.pageRedirects[title] = {'id':self.id,'redirect':getRedirect(self.text)}
    self.talkpages[title] = {'id':self.id,'projects':getProjects(self.text)}
    self.templates[title] = {'id':self.id}
    self.templateRedirects[title] = {'id':self.id,'redirect':redirect}
    """
    handler = MediaWikiHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    try:
        parser.parse(filename)
    except SAXException:
        print "caught"
    return handler
