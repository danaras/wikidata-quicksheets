import os, csv
import logging, re
# from fuzzywuzzy import fuzz
from masterSettings import *

def findFromFirstSentence(inputFileName,language, qid, p1, p1Value, titleOriginal, firstSentence):
	lines = []
	found = False
	firstline = True
	popular = ''
	pValueList = []
	fileName = inputFileName+' Outputs/needs human review/output-found-'+pValues[1][1]+'-minCount'+str(minCount)+'-popular'+str(popularCount)+'.csv'
	# outputTXT = open('output-occupation-percentages.txt', 'w')
	outputCSV = open(fileName, 'ab+')
	csvWriter = csv.writer(outputCSV)


	with open('resources/'+pValueListName, 'rU') as f:
		reader = csv.reader(f)
		for line in reader:
			if firstline:    #skip first line
				firstline = False
				continue
			info = list(line)
			if int(info[3]) >= minCount:
				if int(info[3]) >= popularCount[0]:
					popular = '*'
				elif int(info[3]) >= popularCount[1]:
					popular = '.'
				else:
					popular = ' '
				qidLink = info[0].split('/')
				pqid = qidLink[len(qidLink)-1]
				pValueAlts= []
				alt = info[4].split(', ')
				pValueAlts.extend(alt)
				pValueList.append([info[1],pValueAlts,pqid,popular,info[2]])
	# logging.info(pValueList)
	firstSentence = str(firstSentence)
	logging.info("----------------------------------\n"+firstSentence+"\n------------------------------------\n")
	# outputTXT.write("----------------------------------------\n"+firstSentence+"\n")
	for index, x in enumerate(pValueList):
		# print x[0]
		searchKeywordMain = re.search(r'\b'+re.escape(x[0])+r'\b',firstSentence, re.IGNORECASE)

		if searchKeywordMain:
			found = True
			p2Value = x[0]
			p2 = x[2]
			if os.stat(fileName).st_size == 0:
				# csvWriter.writerow(['QID of person', 'P106', 'QID of occupation', 'stated in', 'enwiki'])
				csvWriter.writerow(rowEdit)
			csvWriter.writerow([language,titleOriginal,qid,p1,p1Value,p2,x[3],"",p2Value,x[4],'',firstSentence])
			readerDuplicate = open(fileName, "r")
			for row in readerDuplicate:
				if row in lines:
					continue
				else:
					lines.append(row)

			writerDuplicate = open(fileName, "w")
			for line in lines:
				writerDuplicate.write(line)
			writerDuplicate.close()
			outputCSV.flush()
		else:
			# print x[1]
			for value in x[1]:
				searchKeywordAlt = re.search(r'\b'+re.escape(value)+r'\b',firstSentence, re.IGNORECASE)
				if searchKeywordAlt and value:
					logging.critical("Found in first sentence: "+value+" ---->> "+firstSentence)
					found = True
					p2Value = x[0]
					p2 = x[2]
					if os.stat(fileName).st_size == 0:
						# csvWriter.writerow(['QID of person', 'P106', 'QID of occupation', 'stated in', 'enwiki'])
						csvWriter.writerow(rowEdit)
					csvWriter.writerow([language,titleOriginal,qid,p1,p1Value,p2,x[3],"",p2Value,x[4],'',firstSentence])
					readerDuplicate = open(fileName, "r")
					for row in readerDuplicate:
						if row in lines:
							continue
						else:
							lines.append(row)

					writerDuplicate = open(fileName, "w")
					for line in lines:
						writerDuplicate.write(line)
					writerDuplicate.close()
					outputCSV.flush()
	return found
