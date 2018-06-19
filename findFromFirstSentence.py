import os, csv
import logging
# from fuzzywuzzy import fuzz
from settings import *
from variables import *


def findFromFirstSentence(inputFileName,language, qid, titleOriginal, firstSentence):
	lines = []
	found = False
	firstline = True
	popular = ''
	pValueList = []
	fileName = inputFileName+' Outputs/needs human review/output-found-'+pValues[1][1]+'-minCount'+str(minCount)+'-popular'+str(popularCount)+'.csv'
	# outputTXT = open('output-occupation-percentages.txt', 'w')
	outputCSV = open(fileName, 'ab+')
	csvWriter = csv.writer(outputCSV)


	with open(pValueListName+'.csv', 'r') as f:
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
				pValueList.append([info[1],pqid,popular,info[2]])
	# logging.info(occupations)
	firstSentence = str(firstSentence)
	logging.info("----------------------------------\n"+firstSentence+"\n------------------------------------\n")
	# outputTXT.write("----------------------------------------\n"+firstSentence+"\n")
	for index, x in enumerate(pValueList):
		if x[0] in firstSentence:
			found = True
			p2Value = x[0]
			p2 = x[1]
			if os.stat(fileName).st_size == 0:
				# csvWriter.writerow(['QID of person', 'P106', 'QID of occupation', 'stated in', 'enwiki'])
				csvWriter.writerow(rowEdit)
			csvWriter.writerow([language,titleOriginal,qid,p1,p1Value,p2,x[2],"",p2Value,x[3],'',firstSentence])
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
