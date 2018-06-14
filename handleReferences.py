#references work with english wikipedia at the moment
import urllib2
import csv
import logging
import html2text
import unicodedata
import cStringIO
import re
from variables import *

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
		nameList = self.convertTitletoList()
		logging.info(nameList)
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
				with open('workfile.txt', 'r') as f2:
					# debugfile = open('debug.txt', 'a+')
					# lines = ''
					prevLine = ''
					for num, line in enumerate(f2):
						nextLine = next(f2)
						lines = prevLine.replace("\n"," ")+line.replace("\n"," ")+nextLine.replace("\n"," ")
						# lines += line.replace("\n"," ")
						# print line
						# logging.info(num)
						if any(name in line for name in nameList):
							# print name
							# print lines
							# debugfile.write("####################################")
							# debugfile.write(lines+"\n")
							# debugfile.flush()
							for keyword in pValueList:
								# logging.info(keyword)
								searchKeyword = re.search(r'\b'+re.escape(keyword)+r'\b',lines, re.IGNORECASE)
								if searchKeyword:
									logging.info("found pValue in Reference link")
									logging.critical(keyword+"--------"+ line+"----------"+link)
									context.append(lines)
						# if (num is not 0) and (num % 3 == 0):
						# 	lines = ''
						prevLine = line
					# debugfile.close()
			except:
				logging.info("error finding keyword########################################")
				# print "something wrong"

		return context

	def openRefLink(self, links):
		linkandContext = {}
		for link in links:
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
		logging.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		logging.info(linkandContext)
		return linkandContext

	def findReferences(self, text):
		logging.info("####################################")
		logging.info(self.title)
		refLinks = []
		# foundRef.write(name+'\n')
		inReferences = False
		f = open('workfileWP.txt', 'w')
		f.write(text)
		f.close()
		with open('workfileWP.txt', 'r') as f2:
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
			response = urllib2.urlopen(WPlink + title, timeout=5)
			html = unicode(response.read(), errors = 'ignore')
			html = unicodedata.normalize('NFKD', html).encode('ascii','ignore')
			return html
		except urllib2.URLError, e:
			logging.info(e)
			logging.info("error reaching wikipedia page for references")

# uncomment the following lines to test the class
# allInfo = {}
# if debug:
# 	outlevel = logging.DEBUG
# else:
#
# 	outlevel = logging.CRITICAL
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p: ')
# logging.getLogger().setLevel(outlevel)
#
# occupation = "African Americans"
# lala = References("JR Hutson", occupation, "pList.csv")
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
