# This class handles all wikipedia data.
from urllib2 import Request, urlopen, URLError
import json
import re
class parseWikipedia():
	def __init__(self,language, titleWP):
		self.language = language
		self.titleWP = titleWP

	def getRedirect(self):
		redirect = Request('https://'+self.language+'.wikipedia.org/w/api.php?action=query&titles='+self.titleWP+'&redirects=yes&format=json')
		try:
			responsePWRedirect = urlopen(redirect, timeout=5)
			wikiPediaRedirect = responsePWRedirect.read()
			jsonDataPWRedirect = json.loads(wikiPediaRedirect)
			try:
				titleRedirect = jsonDataPWRedirect["query"]["redirects"][0]["to"]
				self.titleWP = titleRedirect.encode('utf8').replace(' ', '%20')
				return self.titleWP
			except:
				print "redirect title couldn't be found"
				self.titleWP = self.titleWP.replace(' ', '%20')
				return self.titleWP
		except:
			print "something went wrong getting the redirect title page"
			self.titleWP = self.titleWP.replace(' ', '%20')
			return self.titleWP

	def getWikipediaJSON(self):
		wpRequest = Request('https://'+self.language+'.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+self.titleWP)
		print 'https://'+self.language+'.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+self.titleWP
		#https://en.wikipedia.org/w/api.php?action=query&titles=Elodie%20Courter&redirects=yes
		try:
			responsePW = urlopen(wpRequest, timeout=5)
			wikiPedia = responsePW.read()
			jsonDataPW = json.loads(wikiPedia)
			self.json = jsonDataPW
		except:
			print "cannot get wikipedia 'extract' json object"

	def getFirstSentence(self):
		try:
			keys = self.json["query"]["pages"].keys()
			extract = self.json["query"]["pages"][keys[0]]["extract"]
			print extract
			firstSentence = re.search(r'^.*?\w\w+\)?\.', extract).group(0).encode("utf8")
			print firstSentence
			self.firstSentence = firstSentence
			return firstSentence
		except:
			print "problem getting first sentence"

	def getReferences(self):
		print "getting ref"
lala = parseWikipedia("en", "Mako%20Idemitsu")
title = lala.getRedirect()
print title
lala.getWikipediaJSON()
print lala.json
lalasentence = lala.getFirstSentence()
print lalasentence
