import csv
# from fuzzywuzzy import fuzz
from library.masterSettings import *

wikipedias = wikipediaOptions

class QuickStatement:
	def __init__(self):
		self.name = inputFileNameForQuickStatements
		self.pValueList = []
	def openCSVtoWrite(self):
		if nonWikiRef:
			self.outputCSVRef = open(self.name[:-4]+'-output-ref-qs.txt', 'w')
			self.csvWriterRef = csv.writer(self.outputCSVRef, delimiter = '	')
			self.csvWriterRef.writerow(rowQSRef)
		else:
			self.outputCSV = open(self.name[:-4]+'-output-qs.txt', 'w')
			self.csvWriter = csv.writer(self.outputCSV, delimiter = '	')
			self.csvWriter.writerow(rowQSallWP)

			self.outputCSVALT = open(self.name[:-4]+'-output-alt'+myProperty[1]+'.csv', 'w')
			self.csvWriterALT = csv.writer(self.outputCSVALT)
			self.csvWriterALT.writerow(rowEdit)

			self.outputCSVNEW = open(self.name[:-4]+'-output-NEW'+myProperty[1]+'.csv', 'w')
			self.csvWriterNEW = csv.writer(self.outputCSVNEW)
			self.csvWriterNEW.writerow(rowEdit)

			# self.debugcsv = open('lalallalala.csv', 'w')
			# self.debugwrite = csv.writer(self.debugcsv)
			# self.debugwrite.writerow(['valueLabel','qid','popular','description'])

	def preparePValueList(self):
		self.pValueList = []
		with open('resources/'+pValueListName, 'rU') as f:
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
					# self.debugwrite.writerow([info[1],qid,popular,info[2]])
#if it throws an error saying "_csv.Error: new-line character seen in unquoted field -
#do you need to open the file in universal-newline mode?"
#then you should save the document as plan text csv file again
	def parseInputFile(self):
		with open(self.name,'rU') as csvFile:
			self.openCSVtoWrite()
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
							self.csvWriterRef.writerow([info[2],pValues[1][0],info[5],statedIn,info[8]])
				else:
					if info[7]:
						# if "new" in info[8]:
						# 	print "new found"
						# 	self.csvWriterNEW.writerow([info[0],info[1],info[2],info[3],info[4],"",x[3],x[2],"",info[10],"",info[11]])
						# else:
						for x in wikipedias:
							if x[0] in info[0]:
								wikipediaQID = x[1]
							else:
								wikipediaQID = wpEn
						self.csvWriter.writerow([info[2], propertyId, info[5], referencedIn, wikipediaQID])
					if info[10]:
						for x in wikipedias:
							if x[0] in info[0]:
								wikipediaQID = x[1]
							else:
								wikipediaQID = wpEn
						self.preparePValueList()
						# print info[10]
						for index, x in enumerate(self.pValueList):
							if x[0] == info[10]:
								p2Value = x[0]
								p2QID = x[1]
								# print str(index) + "---"+str(info[1])+"---"+str(p2Value)
								# print x
								self.csvWriterALT.writerow([info[0],info[1],info[2],info[3],info[4],p2QID,x[2],"",p2Value,x[3],info[10],info[11]])
								self.csvWriter.writerow([info[2], propertyId, p2QID, referencedIn, wikipediaQID])

					wikipediaQID = ''
if __name__ == "__main__":
	QS = QuickStatement()
	QS.parseInputFile()
