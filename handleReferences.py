#references work with english wikipedia at the moment
import urllib2
import csv
import logging
import html2text
import unicodedata
import cStringIO
import re


#TODO ask about where References class should be used, because it will slow the code a lot.
class References:
	def __init__(self, title, pValue, plistName):
		self.title = title
		self.pValue = pValue
		self.refLinks = []
		self.plistName = plistName

	def getAsKnownAs(self):
		pValueList = []
		firstline = True
		with open(self.plistName, 'r') as f:
			reader = csv.reader(f)
			for line in reader:
				if firstline:    #skip first line
					firstline = False
					continue
				info = list(line)
				if self.pValue == info[1]:
					pValueList.append(info[1])
					logging.info(info[4])
					alt = info[4].split(", ")
					pValueList.extend(alt)
		return pValueList
	def findKeyword(self, text):
		pValueList = self.getAsKnownAs()
		logging.info(pValueList)
		context = []
		if text:
			f = open('workfile.txt', 'w')
			try:
				cleanText = html2text.html2text(text)
				cleanText = unicodedata.normalize('NFKD', cleanText).encode('ascii','ignore')
				output = cStringIO.StringIO()
				output.write(cleanText)
				content = output.getvalue()
				f.write(content)
				f.close()
				f2 = open('workfile.txt', 'r')
				for line in f2:
					for keyword in pValueList:
						if keyword.lower() in line.lower():
							logging.info("found pValue in Reference link")
							logging.info(keyword+"--------"+ line)
							context.append(line)
			except:
				logging.info("error finding keyword")

		return context

	def openRefLink(self, links):
		linkandContext = {}
		for link in links:
			logging.info(link)
			context = []
			try:
				response = urllib2.urlopen(link)
				html = unicode(response.read(), errors = 'ignore')
				# logging.info(html)
			except :
				# logging.info(e)
				logging.info("error, so skipping this one")
				continue
			html = unicodedata.normalize('NFKD', html).encode('ascii','ignore')
			context = self.findKeyword(html)
			linkandContext[link] = context
		logging.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		logging.info(linkandContext)
		return linkandContext

	def findReferences(self, text):
		logging.info("####################################")
		logging.info(self.title)
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
				logging.info("in references")
			if inReferences:
				link = re.search(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',line)
				if link:
					refLinks.append(link.group())
				if '</ol>' in line:
					inReferences = False
					logging.info("out of references")
		return refLinks

	def getWikiHTML(self):
		title = self.title.replace(' ', '_')
		WPlink = "https://en.wikipedia.org/wiki/"
		logging.info(WPlink + title)
		try:
			response = urllib2.urlopen(WPlink + title)
			html = unicode(response.read(), errors = 'ignore')
			html = unicodedata.normalize('NFKD', html).encode('ascii','ignore')
			return html
		except urllib2.URLError, e:
			logging.info(e)
			logging.info("error reaching wikipedia page for references")

# uncomment the following lines to test the class
# allInfo = {}
# occupation = "african-american"
# lala = References("Deval Patrick", occupation)
# laHTML = lala.getWikiHTML()
# # logging.info(laHTML)
# laLinks = lala.findReferences(laHTML)
# # logging.info(laLinks)
# allInfo = lala.openRefLink(laLinks)
# logging.info(allInfo)
# for link in laLinks:
# 	if link in allInfo:
# 		for context in allInfo[link]:
# 			logging.info(occupation + " ------------ " + link + " -------- " + context)
