from urllib2 import Request, urlopen, URLError
import os, json, csv
import re
from QIDfromCategories import getQidFromCategories
from findOccupation import findOccupationFirstSentence

inputFileName = 'pre2017-improved'
matrixName = '_QID_matrix_output_mar23.csv'
matrixGrepName = '_QID_matrixGREP_output_mar23.csv'
grep = True
title =''
language =''
qid=''
entitiesFound = False
firstSentence = ''
p21 = ''
p106 = ''
gender = ''
occupation = ''
firstline = True

def getWikiData(language, title):
	request = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&sites='+language+'wiki&titles='+title+'&languages='+language+'&props=claims%7Clabels&format=json')
	try:
		response = urlopen(request, timeout=5)
		wikiData = response.read()
		jsonData = json.loads(wikiData)
		return jsonData
	except:
	    print 'General error. Got an error code:'

def getQID(jsonObject):
	try:
		keys = jsonObject["entities"].keys()
		entitiesFound = True
		for key in keys:
			_qid = key
		print _qid
		return _qid
	except:
		print "cannot find entities"


def getRedirect(language, titleWP):
	redirect = Request('https://'+language+'.wikipedia.org/w/api.php?action=query&titles='+titleWP+'&redirects=yes&format=json')
	try:
		responsePWRedirect = urlopen(redirect, timeout=5)
		wikiPediaRedirect = responsePWRedirect.read()
		jsonDataPWRedirect = json.loads(wikiPediaRedirect)
		try:
			titleRedirect = jsonDataPWRedirect["query"]["redirects"][0]["to"]
			return titleRedirect.encode('utf8')
		except:
			print "redirect title couldn't be found"
			return titleWP.replace('%20', ' ')
	except:
		print "something went wrong getting the redirect title page"
		return titleWP.replace('%20', ' ')
if not os.path.exists(inputFileName+" Outputs"):
	os.makedirs(inputFileName+" Outputs")
if not os.path.exists(inputFileName+" Outputs/already has P106"):
	os.makedirs(inputFileName+" Outputs/already has P106")
if not os.path.exists(inputFileName+" Outputs/needs human review"):
	os.makedirs(inputFileName+" Outputs/needs human review")
#output file for female with occupation
outputFemaleGood = open(inputFileName+' Outputs/already has P106/good.csv', 'w')
csvWriterFemaleGood = csv.writer(outputFemaleGood)
csvWriterFemaleGood.writerow(['language','title','QID','p21','gender','p106','occupation','pw first sentence'])
#output file for female with no occupation
outputFemaleLack = open(inputFileName+' Outputs/needs human review/needs-occupation.csv', 'w')
csvWriterFemaleLack = csv.writer(outputFemaleLack)
csvWriterFemaleLack.writerow(['language','title','QID','p21','gender','p106','occupation','pw first sentence'])
#output file for other
outputOther = open(inputFileName+' Outputs/needs human review/output-other.csv', 'w')
csvWriterOther = csv.writer(outputOther)
csvWriterOther.writerow(['language','title','QID','p21','gender','p106','occupation','pw first sentence'])
#output file for has wikipedia but no wikidata
outputOtherNoWD = open(inputFileName+' Outputs/needs human review/output-hasWP-noWD.csv', 'w')
csvWriterOtherNoWD = csv.writer(outputOtherNoWD)
csvWriterOtherNoWD.writerow(['language','title','QID','p21','gender','p106','occupation','pw first sentence'])
#output file for likely deleted
outputOtherDeleted = open(inputFileName+' Outputs/needs human review/output-likelyDeleted.csv', 'w')
csvWriterOtherDeleted = csv.writer(outputOtherDeleted)
csvWriterOtherDeleted.writerow(['language','title','QID','p21','gender','p106','occupation','pw first sentence'])


with open(inputFileName+'.csv','rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		if firstline:    #skip first line
			firstline = False
			continue
		info = list(row)
		# langTitle = info[0]
		try:
			language = info[0]
		except:
			print "no lang found"
		# titleOriginal = langTitle.split(':')[1]
		try:
			titleOriginal = info[1]
			title = titleOriginal.replace(' ', '+')
			print language
			print title
			titleWP=titleOriginal.replace(' ', '%20')
			print titleWP
		except:
			print "title couldn't be read from input file"
		jsonData = getWikiData(language, title)
		if jsonData:
			qid =getQID(jsonData)
		if qid:
			if str(qid) == "-1":
				titleOriginal = getRedirect(language, titleWP)
				if titleOriginal:
					titleWP = titleOriginal.replace(' ', '%20')
					title =  titleOriginal.replace(' ', '+')
					jsonData = getWikiData(language, title)
					qid = getQID(jsonData)

		wpRequest = Request('https://'+language+'.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+titleWP)
		#https://en.wikipedia.org/w/api.php?action=query&titles=Elodie%20Courter&redirects=yes
		try:
			responsePW = urlopen(wpRequest, timeout=5)
			wikiPedia = responsePW.read()
			jsonDataPW = json.loads(wikiPedia)
			try:
				keys = jsonDataPW["query"]["pages"].keys()
				extract = jsonDataPW["query"]["pages"][keys[0]]["extract"]
				print extract
				firstSentence = re.search(r'^.*?\w\w+\)?\.', extract).group(0).encode("utf8")

				print firstSentence
			except:
				print "cannot find extract"
		except:
			print "erroor"
		try:
			p21 = (jsonData["entities"][qid]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"])
			print jsonData["entities"][qid]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"]
		except:
			print "no p21"
		try:
			p106 = (jsonData["entities"][qid]["claims"]["P106"][0]["mainsnak"]["datavalue"]["value"]["id"])
			print jsonData["entities"][qid]["claims"]["P106"][0]["mainsnak"]["datavalue"]["value"]["id"]
		except:
			print "no p106"
		if p21:
			pRequest = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+p21+'&props=descriptions%7Clabels&languages=en&format=json')
			try:
				pResponse = urlopen(pRequest, timeout=5)
				pData = pResponse.read()
				pJsonData = json.loads(pData)
				# print pJsonData
				# print pJsonData["entities"][x]["labels"]["en"]["value"]
				gender = pJsonData["entities"][p21]["labels"]["en"]["value"].encode("utf8")
				print gender
			except:
			    print 'No kittez. Got an error code:'
		if p106:
			pRequest = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+p106+'&props=descriptions%7Clabels&languages=en&format=json')
			try:
				pResponse = urlopen(pRequest, timeout=5)
				pData = pResponse.read()
				pJsonData = json.loads(pData)
				# print pJsonData
				# print pJsonData["entities"][x]["labels"]["en"]["value"]
				if "en" in pJsonData["entities"][p106]["labels"].keys():
					occupation = pJsonData["entities"][p106]["labels"]["en"]["value"].encode("utf8")
				else:
					occupation = pJsonData["entities"][p106]["descriptions"]["en"]["value"].encode("utf8")


				print occupation
			except:
				print 'No kittez. Got an error code:'
		if "female" in gender.lower():
			if occupation:
				print "got to the end and should print female with occupation"
				csvWriterFemaleGood.writerow([language, titleOriginal, qid, p21, gender, p106, occupation, firstSentence])
				outputFemaleGood.flush()
			else:
				foundCat = getQidFromCategories(inputFileName,matrixName, False, titleWP, qid, language, p21, gender, firstSentence)
				if not foundCat:
					foundGrepCat = getQidFromCategories(inputFileName,matrixGrepName, True, titleWP, qid, language, p21, gender, firstSentence)
					if not foundGrepCat:
						foundFirstSentence = findOccupationFirstSentence(inputFileName,language, qid, titleOriginal, p21, gender, firstSentence)
						if not foundFirstSentence:
							csvWriterFemaleLack.writerow([language, titleOriginal, qid, p21, gender, p106, occupation, firstSentence])
							outputFemaleLack.flush()
		else:
			if str(qid) == "-1":
				if firstSentence:
					csvWriterOtherNoWD.writerow([language, titleOriginal, qid, p21, gender, p106, occupation, firstSentence])
					outputOtherNoWD.flush()
				else:
					csvWriterOtherDeleted.writerow([language, titleOriginal, qid, p21, gender, p106, occupation, firstSentence])
					outputOtherDeleted.flush()
			else:
				csvWriterOther.writerow([language, titleOriginal, qid, p21, gender, p106, occupation, firstSentence])
				outputOther.flush()

		keys = []
		qid = ''
		p21 = ''
		p106 = ''
		language = ''
		titleOriginal = ''
		gender = ''
		occupation = ''
		firstSentence = ''
		jsonData = ''
