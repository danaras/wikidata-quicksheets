import csv, json
from urllib2 import Request, urlopen, URLError
inputFileName = 'occupations to sort green or red.csv'
outputCSV = open(inputFileName[:-4]+'-withDescriptions.csv', 'w')
csvWriter = csv.writer(outputCSV)

def getQIDValue(QID):
	if QID:
		pRequest = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+QID+'&props=labels&languages=en&format=json')
		try:
			pResponse = urlopen(pRequest, timeout=5)
			pData = pResponse.read()
			pJsonData = json.loads(pData)
			print pJsonData
			print pJsonData["entities"][QID]["labels"]["en"]["value"]
			if "en" in pJsonData["entities"][QID]["labels"].keys():
 				pValue= pJsonData["entities"][QID]["labels"]["en"]["value"].encode("utf8")
			else:
				pValue = pJsonData["entities"][QID]["descriptions"]["en"]["value"].encode("utf8")
			# print occupation
			return pValue
		except:
			return ""
			print 'No pValue'

def getQIDdescription(qid):
	request = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+qid+'&languages=en&format=json')
	try:
		response = urlopen(request)
		wikiData = response.read()
		jsonData = json.loads(wikiData)
	except:
		print "something went wrong"
	try:
		description = (jsonData["entities"][qid]["descriptions"]["en"]["value"])
		print description
		return description
	except:
		return ""
		print "no description"
def processFile(inputFileName, qidColumn, titleColumn):
	firstline = True
	with open(inputFileName) as csvFile:
		reader = csv.reader(csvFile)
		for row in reader:
			if firstline:    #skip first line
				info = list(row)
				info.insert(titleColumn+1,"description")
				csvWriter.writerow(info)
				firstline = False
				continue
			info = list(row)
			qid = info[qidColumn]
			description = getQIDdescription(qid)
			title = getQIDValue(qid)
			info[titleColumn]=title

			info.insert(titleColumn+1,description.encode('ascii','ignore'))

			csvWriter.writerow(info)
			outputCSV.flush()

processFile(inputFileName,1,2)
