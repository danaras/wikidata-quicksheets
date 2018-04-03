import csv
# from fuzzywuzzy import fuzz
from settings import SettingsForQS

setup = SettingsForQS()
wikipedias = setup.wikipediaOptions
minCount = setup.minCount
popularCount = setup.popularCountSteps
# accuracy = setup.accuracy

firstlineOccupation = True
firstlineALT = True
occupations = []
wpEn = "Q328"
wikipediaQID = ''
referencedIn = "S143"
propertyId = "P106"
outputCSV = open('output-qs.csv', 'w')
csvWriter = csv.writer(outputCSV)
csvWriter.writerow(['QID','property id','occupationQID','referenced in','wikipediaQID'])

outputCSVALT = open('output-altOccupation-accuracy100.csv', 'w')
csvWriterALT = csv.writer(outputCSVALT)
csvWriterALT.writerow(['language','title','QID','p21','gender','p106','occupation description','popular','accept value','occupation','alt occupation','pw first sentence'])

outputCSVNEW = open('output-NEWOccupation.csv', 'w')
csvWriterNEW = csv.writer(outputCSVNEW)
csvWriterNEW.writerow(['language','title','QID','p21','gender','p106','occupation description','popular','accept value','occupation','alt occupation','pw first sentence'])

with open('occupations-withDescriptions.csv', 'r') as f:
	reader = csv.reader(f)
	for line in reader:
		if firstlineOccupation:    #skip first line
			firstlineOccupation = False
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
			occupations.append([info[1],qid,popular,info[2]])
#if it throws an error saying "_csv.Error: new-line character seen in unquoted field -
#do you need to open the file in universal-newline mode?"
#then you should save the document as csv file again
with open('output-found-occupations-minCount5-popular[997, 100].csv','r') as csvFile:
	reader = csv.reader(csvFile)
	for row in reader:
		if firstlineALT:    #skip first line
			firstlineALT = False
			continue
		info = list(row)
		if info[8]:
			if "new" in info[8]:
				print "new found"
				csvWriterNEW.writerow([info[0],info[1],info[2],info[3],info[4],"",x[3],x[2],"",occupation,"",info[11]])
			else:
				for x in wikipedias:
					if x[0] in info[0]:
						wikipediaQID = x[1]
					else:
						wikipediaQID = wpEn
				csvWriter.writerow([info[2], propertyId, info[5], referencedIn, wikipediaQID])
		if info[10]:
			for index, x in enumerate(occupations):
				if x[0] == info[10]:
					occupation = x[0]
					occupationQID = x[1]
					csvWriterALT.writerow([info[0],info[1],info[2],info[3],info[4],occupationQID,x[3],x[2],"",occupation,info[10],info[11]])
					csvWriter.writerow([info[2], propertyId, occupationQID, referencedIn, wikipediaQID])

		wikipediaQID = ''
