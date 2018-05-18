# This is the class that pulls and parses wikidata.
from urllib2 import Request, urlopen, URLError
import json
import re

class parseWikidata:
	def __init__(self,language,title):
		self.language = language
		self.title = title
		self.pData = {}
	def getWikiData(self):
		request = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&sites='+self.language+'wiki&titles='+self.title+'&languages='+self.language+'&props=claims%7Clabels&format=json')
		print 'https://www.wikidata.org/w/api.php?action=wbgetentities&sites='+self.language+'wiki&titles='+self.title+'&languages='+self.language+'&props=claims%7Clabels&format=json'
		try:
			response = urlopen(request, timeout=5)
			wikiData = response.read()
			jsonData = json.loads(wikiData)
			self.jsonData = jsonData
			return jsonData
		except:
		    print 'General error. Cannot get the wikidata json'

	def getQID(self):
		try:
			keys = self.jsonData["entities"].keys()
			entitiesFound = True
			for key in keys:
				qid = key
				self.qid = qid
				return qid
		except:
			print "cannot find entities"
	def getPData(self, pID):
		try:
			pQID = (self.jsonData["entities"][self.qid]["claims"][pID][0]["mainsnak"]["datavalue"]["value"]["id"])
			print self.jsonData["entities"][self.qid]["claims"][pID][0]["mainsnak"]["datavalue"]["value"]["id"]
			if pQID:
				pRequest = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+pQID+'&props=descriptions%7Clabels&languages=en&format=json')
				try:
					pResponse = urlopen(pRequest, timeout=5)
					pData = pResponse.read()
					pJsonData = json.loads(pData)
					# print pJsonData
					# print pJsonData["entities"][x]["labels"]["en"]["value"]
					if "en" in pJsonData["entities"][pQID]["labels"].keys():
		 				pValue= pJsonData["entities"][pQID]["labels"]["en"]["value"].encode("utf8")
					else:
						pValue = pJsonData["entities"][pQID]["descriptions"]["en"]["value"].encode("utf8")
					self.pData[pID] = [pQID, pValue]
					print self.pData
					return [pID, pQID, pValue]
				except:
					print 'No pValue'
					self.pData[pID] = [pQID, '']
					return [pID, pQID, '']
		except:
			print "no pqid"
			self.pData[pID] = ['', '']
			return [pID, '', '']
