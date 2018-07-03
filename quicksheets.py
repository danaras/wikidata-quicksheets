#This is the main script that manages all the classes and methods
#The input file is parsed here and output file is written here as well
from urllib2 import Request, urlopen, URLError
import os, json, csv

import re
import logging, sys
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p: ')

from library.masterSettings import *
from library.QIDfromCategories import getQidFromCategories
from library.findFromFirstSentence import findFromFirstSentence
from library.parseWikidata import parseWikidata
from library.parseWikipedia import parseWikipedia
from library.handleReferences import References

print debug
if debug:
	outlevel = logging.DEBUG
else:

	outlevel = logging.CRITICAL

logging.getLogger().setLevel(outlevel)

inputFileName = inputFileNameQuickSheets


logging.debug('A debug message!')
#make a module for this whole section where you are creating directories and output files
if not os.path.exists(inputFileName+" Outputs"):
	os.makedirs(inputFileName+" Outputs")
if not os.path.exists(inputFileName+" Outputs/already has "+pValues[1][0]):
	os.makedirs(inputFileName+" Outputs/already has "+pValues[1][0])
if not os.path.exists(inputFileName+" Outputs/needs human review"):
	os.makedirs(inputFileName+" Outputs/needs human review")
#output file for female with p2Va
outputFemaleGood = open(inputFileName+' Outputs/already has '+pValues[1][0]+'/good.csv', 'w')
csvWriterFemaleGood = csv.writer(outputFemaleGood)
csvWriterFemaleGood.writerow(rowHuman)
#output file for female with no p2Va
outputFemaleLack = open(inputFileName+' Outputs/needs human review/needs-'+pValues[1][1]+'.csv', 'w')
csvWriterFemaleLack = csv.writer(outputFemaleLack)
csvWriterFemaleLack.writerow(rowHuman)
#output file for other
outputOther = open(inputFileName+' Outputs/needs human review/output-other.csv', 'w')
csvWriterOther = csv.writer(outputOther)
csvWriterOther.writerow(rowHuman)
#output file for has wikipedia but no wikidata
outputOtherNoWD = open(inputFileName+' Outputs/needs human review/output-hasWP-noWD.csv', 'w')
csvWriterOtherNoWD = csv.writer(outputOtherNoWD)
csvWriterOtherNoWD.writerow(rowHuman)
#output file for likely deleted
outputOtherDeleted = open(inputFileName+' Outputs/needs human review/output-likelyDeleted.csv', 'w')
csvWriterOtherDeleted = csv.writer(outputOtherDeleted)
csvWriterOtherDeleted.writerow(rowHuman)

if getReferences:
	outputRef = open(inputFileName+' Outputs/needs human review/output-references.csv', 'w')
	csvWriterRef = csv.writer(outputRef)
	csvWriterRef.writerow(rowRef)

#open the input file as a csv file
with open(inputFileName+'.csv','rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		qid = ''
		info = list(row)
		if firstline:
			if 'qid' in info[0].lower():
				qidDocument = True
			else:
				qidDocument = False
			   #skip first line
			firstline = False
			continue
		# langTitle = info[0]
		try:
			if qidDocument:
				language = "en"
				qid = info[0].replace('wd:','')
			else:
				language = info[0] #get the language
		except:
			logging.info("no lang found")
		# titleOriginal = langTitle.split(':')[1]
		try:
			titleOriginal = info[1] #get the title
			title = titleOriginal.replace(' ', '+') #format the title for wikidata api query
			logging.info(language)
			logging.critical("##########################################")
			logging.critical(titleOriginal)
			titleWP=titleOriginal.replace(' ', '%20') #format the title for wikipedia api query
			logging.info(titleWP)
		except:
			logging.info("title couldn't be read from input file")
		WD = parseWikidata(language,title,qid,qidDocument) #call the wikidata parsing class
		WP = parseWikipedia(language,titleWP) #call the wikipedia parsing class
		jsonData = WD.getWikiData() #get the wikidata json object
		if jsonData and qidDocument==False:
			qid = WD.getQID() #get the qid for the object
		if qid:
			if str(qid) == "-1": #if the qid returns -1 check if it has a redirect
				titleOriginal = WP.getRedirect()
				if titleOriginal: #if there is a redirect then update the title formats, the wikidata json object and qid
					titleOriginal = titleOriginal.replace('%20',' ')
					titleWP = titleOriginal.replace(' ', '%20')
					title =  titleOriginal.replace(' ', '+')
					jsonData = WD.getWikiData()
					qid = WD.getQID()
		WP.getWikipediaJSON() #get wikipedia json object
		if useFirstSentence:
			firstSentence = WP.getFirstSentence()
		WD.getPData(pValues[0][0])
		WD.getPData(pValues[1][0])
		logging.info(WD.pData)
		# logging.info(pList21)
		p1 = WD.pData[pValues[0][0]][0].decode().encode('utf-8')

		p1Value = WD.pData[pValues[0][0]][1].decode().encode('utf-8')
		p2 = WD.pData[pValues[1][0]][0].decode().encode('utf-8')
		p2Value = WD.pData[pValues[1][0]][1].decode().encode('utf-8')
		print titleOriginal+" --- "+p1+" --- "+p1Value
		if any(p1Value.lower() ==  s.lower() for s in genderSelect):
			if p2Value:
				#if the title is a specified gender and has the secondary P value write to the good.csv file
				if getReferences:
					allInfo = {}
					ref = References(titleOriginal, p2Value)
					refHTML = ref.getWikiHTML()
					# logging.info(laHTML)
					refLinks = ref.findReferences(refHTML)
					# logging.info(laLinks)
					allInfo = ref.openRefLink(refLinks)
					logging.info(allInfo)
					for link in refLinks:
						if link in allInfo:
							for context in allInfo[link]:
								logging.info(p2Value + " ------------ " + link + " -------- " + context)
								csvWriterRef.writerow([language, titleOriginal, qid, p1, p1Value, p2, p2Value,'',link, context])
								outputRef.flush()

				csvWriterFemaleGood.writerow([language, titleOriginal, qid, p1, p1Value, p2, p2Value, firstSentence])
				outputFemaleGood.flush()
			else:
				if useCategories:
				#if the title is a specified p1Value and doesn't have the secondary P value check the categories
					foundCat = getQidFromCategories(inputFileName,matrixName, False, titleWP, qid, language, p1, p1Value, firstSentence)
					if not foundCat:
						#if the title is a specified p1Value and doesn't have the secondary P value and not in the categorie, check the  grep categories
						foundGrepCat = getQidFromCategories(inputFileName,matrixGrepName, True, titleWP, qid, language, p1, p1Value, firstSentence)
						if useFirstSentence:
							if not foundGrepCat:
								#if not found in categories then find p2Value through WP first sentence
								foundFirstSentence = findFromFirstSentence(inputFileName,language, qid, p1, p1Value, titleOriginal, firstSentence)
								if not foundFirstSentence:
									csvWriterFemaleLack.writerow([language, titleOriginal, qid, p1, p1Value, p2, p2Value, firstSentence])
									outputFemaleLack.flush()
				else:
					if useFirstSentence:
						foundFirstSentence = findFromFirstSentence(inputFileName,language, qid, p1, p1Value, titleOriginal, firstSentence)
						if not foundFirstSentence:
							csvWriterFemaleLack.writerow([language, titleOriginal, qid, p1, p1Value, p2, p2Value, firstSentence])
							outputFemaleLack.flush()
					else:
						csvWriterFemaleLack.writerow([language, titleOriginal, qid, p1, p1Value, p2, p2Value, firstSentence])
						outputFemaleLack.flush()
		else:
			#if qid is -1 and it is not a redirect then check if there is a first firstSentence
			#because if there is no first sentence it means that the title has been probably deleted
			if str(qid) == "-1":
				if firstSentence:
					csvWriterOtherNoWD.writerow([language, titleOriginal, qid, p1, p1Value, p2, p2Value, firstSentence])
					outputOtherNoWD.flush()
				else:
					csvWriterOtherDeleted.writerow([language, titleOriginal, qid, p1, p1Value, p2, p2Value, firstSentence])
					outputOtherDeleted.flush()
			else:
				csvWriterOther.writerow([language, titleOriginal, qid, p1, p1Value, p2, p2Value, firstSentence])
				outputOther.flush()
		#here we are resetting the following values
		keys = []
		p1 = ''
		p2 = ''
		language = ''
		titleOriginal = ''
		p1Value = ''
		p2Value = ''
		firstSentence = ''
		jsonData = ''
