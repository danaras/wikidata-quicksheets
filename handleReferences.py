#references work with english wikipedia at the moment
import urllib2
import csv
import sys
import html2text
import unicodedata
import cStringIO
import re
#TODO ask about where References class should be used, because it will slow the code a lot.
class References:
	def __init__(self, title, pValue):
		self.title = title
		self.pValue = pValue
		self.refLinks = []

	def findKeyword(self, text):
		context = []
		f = open('workfile.txt', 'w')
		cleanText = html2text.html2text(text)
		cleanText = unicodedata.normalize('NFKD', cleanText).encode('ascii','ignore')
		output = cStringIO.StringIO()
		output.write(cleanText)
		content = output.getvalue()
		f.write(content)
		f.close()
		f2 = open('workfile.txt', 'r')
		for line in f2:
			if self.pValue in line:
				print "found pValue in Reference link"
				context.append(line)
		return context

	def openRefLink(self, links):
		linkandContext = {}
		for link in links:
			context = []
			try:
				response = urllib2.urlopen(link)
				html = unicode(response.read(), errors = 'ignore')
				# print html
			except urllib2.URLError, e:
				print e
				print "error, so skipping this one"
				continue
			html = unicodedata.normalize('NFKD', html).encode('ascii','ignore')
			context = self.findKeyword(html)
			linkandContext[link] = context
		# print linkandContext
		return linkandContext

	def findReferences(self, text):
		refLinks = []
		# foundRef.write(name+'\n')
		inReferences = False
		f = open('workfile.txt', 'w')
		f.write(text)
		f.close()
		f2 = open('workfile.txt', 'r')
		for line in f2:
			if '<ol class="references">' in line:
				inReferences = True
				print "in references"
			if inReferences:
				link = re.search(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',line)
				if link:
					refLinks.append(link.group())
				if '</ol>' in line:
					inReferences = False
					print "out of references"
		return refLinks

	def getWikiHTML(self):
		title = self.title.replace(' ', '_')
		WPlink = "https://en.wikipedia.org/wiki/"
		print WPlink + title
		try:
			response = urllib2.urlopen(WPlink + title)
			html = unicode(response.read(), errors = 'ignore')
			html = unicodedata.normalize('NFKD', html).encode('ascii','ignore')
			return html
		except urllib2.URLError, e:
			print e
			print "error reaching wikipedia page for references"

# uncomment the following lines to test the class
# allInfo = {}
# occupation = "artist"
# lala = References("Alix Pearlstein", occupation)
# laHTML = lala.getWikiHTML()
# # print laHTML
# laLinks = lala.findReferences(laHTML)
# print laLinks
# allInfo = lala.openRefLink(laLinks)
# print allInfo
# for link in laLinks:
# 	if link in allInfo:
# 		for context in allInfo[link]:
# 			print occupation + " ------------ " + link + " -------- " + context
