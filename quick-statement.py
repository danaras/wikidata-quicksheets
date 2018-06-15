import csv
# from fuzzywuzzy import fuzz
from settings import SettingsForQS
from variables import *

setup = SettingsForQS()
wikipedias = setup.wikipediaOptions
minCount = setup.minCount
popularCount = setup.popularCountSteps

class QuickStatement:
	def __init__(self):
		self.name = inputFileNameQuickStatements
		self.pValueList = []
	def openCSVtoWrite(self):
		if nonWikiRef:
			self.outputCSVRef = open(self.name+'-output-ref-qs.csv', 'w')
			self.csvWriterRef = csv.writer(self.outputCSVRef)
			self.csvWriterRef.writerow(rowQSRef)
		else:
			self.outputCSV = open(self.name+'-output-qs.csv', 'w')
			self.csvWriter = csv.writer(self.outputCSV)
			self.csvWriter.writerow(rowQSallWP)

			self.outputCSVALT = open(self.name+'-output-alt'+pValue[1][1]+'.csv', 'w')
			self.csvWriterALT = csv.writer(self.outputCSVALT)
			self.csvWriterALT.writerow(rowEdit)

			self.outputCSVNEW = open(self.name+'-output-NEW'+pValue[1][1]+'.csv', 'w')
			self.csvWriterNEW = csv.writer(self.outputCSVNEW)
			self.csvWriterNEW.writerow(rowEdit)

	def preparePValueList(self):
		with open(pValueListName+'.csv', 'r') as f:
			firstline = True
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
					qid = qidLink[len(qidLink)-1]
					self.pValueList.append([info[1],qid,popular,info[2]])
#if it throws an error saying "_csv.Error: new-line character seen in unquoted field -
#do you need to open the file in universal-newline mode?"
#then you should save the document as plan text csv file again
	def parseInputFile(self):
		with open(self.name+'.csv','r') as csvFile:
			firstline = True
			reader = csv.reader(csvFile)
			for row in reader:
				if firstline:    #skip first line
					firstline = False
					continue
				info = list(row)
				if nonWikiRef:
					if info[7]:
						if 'y' == info[7]:
							csvWriterRef.writerow([])
				else:
					if info[8]:
						if "new" in info[8]:
							print "new found"
							csvWriterNEW.writerow([info[0],info[1],info[2],info[3],info[4],"",x[3],x[2],"",info[10],"",info[11]])
						else:
							for x in wikipedias:
								if x[0] in info[0]:
									wikipediaQID = x[1]
								else:
									wikipediaQID = wpEn
							csvWriter.writerow([info[2], propertyId, info[5], referencedIn, wikipediaQID])
					if info[10]:
						self.preparePValueList()
						for index, x in enumerate(self.pValueList):
							if x[0] == info[10]:
								p2Value = x[0]
								p2QID = x[1]
								csvWriterALT.writerow([info[0],info[1],info[2],info[3],info[4],p2QID,x[3],x[2],"",p2Value,info[10],info[11]])
								csvWriter.writerow([info[2], propertyId, p2QID, referencedIn, wikipediaQID])

					wikipediaQID = ''

QS = QuickStatement()
QS.parseInputFile()
