from urllib2 import Request, urlopen, URLError
import os, json, csv
import logging
#output from categories:
def outputFiles(inputFileName, qid, occupation, occupationQID,title, language, p21, gender, firstSentence):
	lines = []
	linesQS = []
	output = open(inputFileName+" Outputs/Category Outputs CSV/"+occupation+occupationQID+'.csv', 'ab+')
	csvWriter = csv.writer(output)
	outputQS = open(inputFileName+" Outputs/Category Outputs QS/"+occupation+occupationQID+'.csv', 'ab+')
	csvWriterQS = csv.writer(outputQS)

	# logging.info("length ===================== "+str(os.stat('Category Outputs/'+occupation+occupationQID+'.csv').st_size))
	if os.stat(inputFileName+" Outputs/Category Outputs CSV/"+occupation+occupationQID+'.csv').st_size == 0:
		# csvWriter.writerow(['QID of person', 'P106', 'QID of occupation', 'stated in', 'enwiki'])
		csvWriter.writerow(['language','title','QID','p21','gender','p106','occupation','pw first sentence'])
	csvWriter.writerow([language, title, qid, p21, gender, occupationQID, occupation, firstSentence])
	output.flush()

	readerDuplicate = open(inputFileName+" Outputs/Category Outputs CSV/"+occupation+occupationQID+'.csv', "rb")
	for row in readerDuplicate:
		if row in lines:
			continue
		else:
			lines.append(row)

	writerDuplicate = open(inputFileName+" Outputs/Category Outputs CSV/"+occupation+occupationQID+'.csv', "wb")
	for line in lines:
		writerDuplicate.write(line)
	writerDuplicate.close()

#Write quick statement csv's
	if os.stat(inputFileName+" Outputs/Category Outputs QS/"+occupation+occupationQID+'.csv').st_size == 0:
		csvWriterQS.writerow(['QID of person', 'P106', 'QID of occupation', 'stated in', 'enwiki'])
	csvWriterQS.writerow([qid, 'P106', occupationQID,'S142','Q328'])
	output.flush()

	readerDuplicateQS = open(inputFileName+" Outputs/Category Outputs QS/"+occupation+occupationQID+'.csv', "rb")
	for rowQS in readerDuplicateQS:
		if rowQS in linesQS:
			continue
		else:
			linesQS.append(rowQS)

	writerDuplicateQS = open(inputFileName+" Outputs/Category Outputs QS/"+occupation+occupationQID+'.csv', "wb")
	for lineQS in linesQS:
		writerDuplicateQS.write(lineQS)
	writerDuplicateQS.close()


def getQidFromCategories(inputFileName, matrixName, isItGrep, title, qid,language, p21, gender, firstSentence):
	if not os.path.exists(inputFileName+" Outputs/Category Outputs CSV"):
		os.makedirs(inputFileName+" Outputs/Category Outputs CSV")
	if not os.path.exists(inputFileName+" Outputs/Category Outputs QS"):
		os.makedirs(inputFileName+" Outputs/Category Outputs QS")
	totalFound = False
	outputCat = open(inputFileName+" Outputs/Category Outputs CSV/caughtCategories.txt", 'ab+')
	#declaring variables for matrix file
	matrixInfo = []
	firstlineMatrix = True

	with open('resources/'+matrixName, 'r') as matrixFile:
		reader = csv.reader(matrixFile)
		for line in reader:
			if firstlineMatrix:    #skip first line
				firstlineMatrix = False
				continue
			info = list(line)
			matrixInfo.append(line)
	found = False
	keys = []
	categories = []
	request = Request('https://en.wikipedia.org/w/api.php?action=query&prop=categories&titles='+title+'&format=json')
	try:
		response = urlopen(request, timeout=5)
		wikiData = response.read()
		jsonData = json.loads(wikiData)
	except:
		logging.info('General error while loading api request')
	try:
		keys = jsonData['query']['pages'].keys()
	except:
		logging.info("cannot find page keys")
	try:
		categories=(jsonData['query']['pages'][keys[0]]['categories'])
		logging.info(categories)
	except:
		logging.info("cannot find categories")
	if categories:
		for each in categories:
			outputCat.write(title.replace('%20', ' ')+'\n')
			outputCat.write(each['title'].encode('utf-8')+'\n')
			occupation = ''
			occupationQID = ''
			logging.info(each['title'])
			category = each['title']
			if 'Category:' in category:
				category = category[9:]
			for index, x in enumerate(matrixInfo):

				if isItGrep:
					#outputCat.write("matrix---------------"+x[0].lower()+'\n')
					#outputCat.write("wp-------------------"+category.lower()+'\n')
					# logging.info("matrix---------------"+x[0].lower())
					# logging.info("wp-------------------"+category.lower())
					# logging.info("grep")
					if x[0].lower() in category.lower():

						occupation = x[1]
						occupationQID = x[2]
						#outputCat.write("+++++++++++++++++++++++++++++++"+occupation+"+++++++"+qid+'\n')
						outputFiles(inputFileName,qid, occupation, occupationQID, title.replace('%20',' '), language, p21, gender, firstSentence)
						found = True
					else:
						found = False
						# outputCat.write(category+'\n')
				else:
					if x[0][:-4].lower() == category.lower():
						occupation = x[1]
						occupationQID = x[2]
						outputFiles(inputFileName,qid, occupation, occupationQID, title.replace('%20',' '), language, p21, gender, firstSentence)
						found = True
					else:
						found = False
				if found:
					totalFound = True
	logging.info("*****************************"+str(totalFound))
	return totalFound
