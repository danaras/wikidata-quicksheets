#This is the main script that manages all the classes and methods
#The input file is parsed here and output file is written here as well
from urllib2 import Request, urlopen, URLError
import os, json, csv
import re
from QIDfromCategories import getQidFromCategories
from findOccupation import findOccupationFirstSentence
from parseWikidata import parseWikidata
from parseWikipedia import parseWikipedia
from handleReferences import References
from variables import *
#put into user settings file

#make a module for this whole section where you are creating directories and output files
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

#open the input file as a csv file
with open(inputFileName+'.csv','rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		if firstline:    #skip first line
			firstline = False
			continue
		info = list(row) #get the row as a list
		# langTitle = info[0]
		try:
			language = info[0] #get the language
		except:
			print "no lang found"
		# titleOriginal = langTitle.split(':')[1]
		try:
			titleOriginal = info[1] #get the title
			title = titleOriginal.replace(' ', '+') #format the title for wikidata api query
			print language
			print title
			titleWP=titleOriginal.replace(' ', '%20') #format the title for wikipedia api query
			print titleWP
		except:
			print "title couldn't be read from input file"
		WD = parseWikidata(language,title) #call the wikidata parsing class
		WP = parseWikipedia(language,titleWP) #call the wikipedia parsing class
		jsonData = WD.getWikiData() #get the wikidata json object
		if jsonData:
			qid = WD.getQID() #get the qid for the object
		if qid:
			if str(qid) == "-1": #if the qid returns -1 check if it has a redirect
				titleOriginal = WP.getRedirect()
				if titleOriginal: #if there is a redirect then update the title formats, the wikidata json object and qid
					titleWP = titleOriginal.replace(' ', '%20')
					title =  titleOriginal.replace(' ', '+')
					jsonData = WD.getWikiData()
					qid = WD.getQID()
		WP.getWikipediaJSON() #get wikipedia json object
		firstSentence = WP.getFirstSentence()
		pList21 = WD.getPData("P21")
		pList106 = WD.getPData("P106")
		print WD.pData
		print pList21
		p21 = WD.pData["P21"][0]
		gender = WD.pData["P21"][1]
		p106 = WD.pData["P106"][0]
		occupation = WD.pData["P106"][1]
#"female" becomes a variable and get assigned (m,f,t, all)
		if "female" in WD.pData["P21"][1].lower():
#make p106 as a variable
			if WD.pData["P106"][1]:
				#if the title is a specified gender and has the secondary P value write to the good.csv file

				csvWriterFemaleGood.writerow([language, titleOriginal, qid, p21, gender, p106, occupation, firstSentence])
				outputFemaleGood.flush()
			else:
				#if the title is a specified gender and doesn't have the secondary P value check the categories
				foundCat = getQidFromCategories(inputFileName,matrixName, False, titleWP, qid, language, p21, gender, firstSentence)
				if not foundCat:
					#if the title is a specified gender and doesn't have the secondary P value and not in the categorie, check the  grep categories
					foundGrepCat = getQidFromCategories(inputFileName,matrixGrepName, True, titleWP, qid, language, p21, gender, firstSentence)
					if not foundGrepCat:
						#if not found in categories then find occupation through WP first sentence
						foundFirstSentence = findOccupationFirstSentence(inputFileName,language, qid, titleOriginal, p21, gender, firstSentence)
						if not foundFirstSentence:
							csvWriterFemaleLack.writerow([language, titleOriginal, qid, p21, gender, p106, occupation, firstSentence])
							outputFemaleLack.flush()
		else:
			#if qid is -1 and it is not a redirect then check if there is a first firstSentence
			#because if there is no first sentence it means that the title has been probably deleted
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
		#here we are resetting the following values
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
