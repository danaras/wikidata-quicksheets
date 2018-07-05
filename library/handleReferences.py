#references work with english wikipedia at the moment
import urllib2
import csv
import logging
import html2text
import unicodedata
import cStringIO
import re
from masterSettings import *

#TODO ask about where References class should be used, because it will slow the code a lot.
class References:
	def __init__(self, title, pValue):
		self.title = title
		self.pValue = pValue
		self.refLinks = []
		self.plistName = pValueListName

	def getAsKnownAs(self):
		pValueList = []
		firstline = True
		with open('resources/'+self.plistName, 'r') as f:
			reader = csv.reader(f)
			for line in reader:
				if firstline:    #skip first line
					firstline = False
					continue
				info = list(line)
				if self.pValue == info[1]:
					pValueList.append(info[1])
					logging.info(info[4])
					alt = info[4].split(', ')
					pValueList.extend(alt)
		return pValueList
	def convertTitletoList(self):
		namelist = []
		eliminationList = ['.', '"']
		name = self.title.split(',')
		name = name[0]
		splitName = name.split(' ')
		logging.info(splitName)
		for word in splitName:
			if not any(char in word for char in eliminationList) and len(word)>1 and word[0].isupper():
				namelist.append(word)
		return namelist
	def findKeyword(self, text, link):
		# debugFile = open('debug.txt', 'a+')
		nameList = self.convertTitletoList()
		logging.info(nameList)
		pValueList = self.getAsKnownAs()
		logging.info(pValueList)
		context = []
		if text:
			try:
				cleanText = html2text.html2text(text)
				cleanText = unicodedata.normalize('NFKD', cleanText).encode('ascii','ignore')
				output = cStringIO.StringIO()
				output.write(cleanText)
				content = output.getvalue()
				# prevLine = ''
				textList = filter(None, content.splitlines())
				# print len(textList)
				# str_list = filter(None, str_list)
				for i in range(0,len(textList)):
					if i==0 and i!=len(textList)-1:
						lines = textList[i]+" "+textList[i+1]
					elif i>0 and i+1<len(textList):
						lines = textList[i-1]+" "+textList[i]+" "+textList[i+1]
					elif i==len(textList)-1 and i-1>0:
						lines = textList[i-1]+" "+textList[i]
					else:
						lines = textList[i]
					if any(name in textList[i] for name in nameList):
						# print lines
						for keyword in pValueList:
							# logging.info(keyword)
							searchKeyword = re.search(r'\b'+re.escape(keyword)+r'\b',lines, re.IGNORECASE)
							if searchKeyword:
								logging.info("found pValue in Reference link")
								logging.critical(keyword+"--------"+ lines+"----------"+link)
								context.append(lines)
								# debugFile.write("##################################################################\n")
								# debugFile.write(content)
					# prevLine = line
			except:
				logging.info("error finding keyword########################################")
				# print "something wrong"
		# debugFile.close()
		return context

	def openRefLink(self, links):
		linkandContext = {}
		foundReferences = 0
		for index,link in enumerate(links):
			logging.info(link)
			context = []
			try:
				response = urllib2.urlopen(link, timeout=5)
				html = unicode(response.read(), errors = 'ignore')
				# logging.info(html)
			except :
				# logging.info(e)
				logging.info("error, so skipping this one")
				continue
			html = unicodedata.normalize('NFKD', html).encode('ascii','ignore')
			context = self.findKeyword(html, link)
			linkandContext[link] = context
			if context:
				foundReferences += 1
			if foundReferences == refLinkLimit:
				break
		logging.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		logging.info(linkandContext)
		return linkandContext

	def findReferences(self, text):
		logging.info("####################################")
		logging.info(self.title)
		refLinks = []
		# foundRef.write(name+'\n')
		inReferences = False
		for line in text.splitlines():
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
		return refLinks[:refLinkLimit]

	def getWikiHTML(self):
		title = self.title.replace(' ', '_')
		WPlink = "https://en.wikipedia.org/wiki/"
		logging.info(WPlink + title)
		try:
			response = urllib2.urlopen(WPlink + title, timeout=5)
			html = unicode(response.read(), errors = 'ignore')
			html = unicodedata.normalize('NFKD', html).encode('ascii','ignore')
			return html
		except urllib2.URLError, e:
			logging.info(e)
			logging.info("error reaching wikipedia page for references")

if __name__ == "__main__":
	allInfo = {}
	if debug:
		outlevel = logging.DEBUG
	else:

		outlevel = logging.CRITICAL
	logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p: ')
	logging.getLogger().setLevel(outlevel)

	occupation = "African Americans"
	lala = References("Harriet Hemings", occupation, "pList.csv")
	laHTML = lala.getWikiHTML()
	# logging.info(laHTML)
	laLinks = lala.findReferences(laHTML)
	# logging.info(laLinks)
	allInfo = lala.openRefLink(laLinks)
	logging.info(allInfo)
	for link in laLinks:
		if link in allInfo:
			for context in allInfo[link]:
				logging.info(occupation + " ------------ " + link + " -------- " + context)
