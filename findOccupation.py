import os, csv
# from fuzzywuzzy import fuzz
from settings import SettingsForFindOccupation

def findOccupationFirstSentence(inputFileName,language, qid, titleOriginal, p21, gender, firstSentence):
	lines = []
	found = False
	setup = SettingsForFindOccupation()
	firstline = True
	minCount = setup.minCount
	popularCount = setup.popularCount
	popular = ''
	occupations = []
	fileName = inputFileName+' Outputs/needs human review/output-found-occupations-minCount'+str(minCount)+'-popular'+str(popularCount)+'.csv'
	# outputTXT = open('output-occupation-percentages.txt', 'w')
	outputCSV = open(fileName, 'ab+')
	csvWriter = csv.writer(outputCSV)


	with open('occupations-withDescriptions.csv', 'r') as f:
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
				occupQID = qidLink[len(qidLink)-1]
				occupations.append([info[1],occupQID,popular,info[2]])
	# print occupations
	firstSentence = str(firstSentence)
	print "----------------------------------\n"+firstSentence+"\n------------------------------------\n"
	# outputTXT.write("----------------------------------------\n"+firstSentence+"\n")
	for index, x in enumerate(occupations):
		if x[0] in firstSentence:
			found = True
			occupation = x[0]
			occupationQID = x[1]
			if os.stat(fileName).st_size == 0:
				# csvWriter.writerow(['QID of person', 'P106', 'QID of occupation', 'stated in', 'enwiki'])
				csvWriter.writerow(['language','title','QID','p21','gender','p106','popular','accept value','occupation','occupation description','alt occupation','pw first sentence'])
			csvWriter.writerow([language,titleOriginal,qid,p21,gender,occupationQID,x[2],"",occupation,x[3],'',firstSentence])
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
