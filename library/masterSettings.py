from userSettings import *
debug = False
qidDocument = False
minCount = 5
refLinkLimit = 20
popularCount = [997,100]
wikipediaOptions = [["en","Q328"],["es","Q8449"],["de","Q48183"],["fr","Q8447"],["pt","Q11921"]]
genderPValues = [['P21','gender']]

wpEn = "Q328"
wikipediaQID = ''
referencedIn = "S143"
propertyId = "P106"
statedIn = 'P248'
firstline = True
title =''
language =''
qid=''
firstSentence = ''

entitiesFound = False

useFirstSentence = False
useCategories = False
getReferences = False



if searchFirstSentence == True:
	#set all of the useVariables here
	useFirstSentence = True
if lookForReferences == True:
	#set all of the useVariables here
	getReferences = True

if matchCategories == True:
	#set all of the useVariables here
	useCategories = True
	matrixName = '_'+myProperty[0]+'_QID_matrix.csv'
	grep = True
	matrixGrepName = '_'+myProperty[0]+'_QID_matrix_GREP.csv'


# Variables only for quicksheets.py
inputFileNameQuickSheets = inputFileNameQuickSheets[:-4]
pValues = genderPValues.append(myProperty)
pValues = genderPValues
genderSelect = []
if cisMen:
	genderSelect.append("male")
if cisWomen:
	genderSelect.append("female")
if transExpansive:
	genderSelect.append("transgender female")
	genderSelect.append("transgender male")
	genderSelect.append("non-binary")
	genderSelect.append("intersex")
	genderSelect.append("transgender")
	genderSelect.append("hermaphrodite")
	genderSelect.append("neutral sex")

# If you want to use categories edit the following field ########################

# If you want to use the WP first sentence edit the following field ##############

# Variables both for quicksheets.py and quick-statement.py ##############
pValueListName = 'list_of_all_items_in_'+myProperty[0]+'.csv'
refLinkLimit = 5

# Variables only for quick-statement.py #####################################
nonWikiRef = getReferences
#Alex Pearlstein, Q19592455, P106, Video Artist, Q18216771, P248, http://artsatl.com/review-19/, Review: At Contemporary, video artist Alix Pearlstein leaves the ordinary

#don't edit below here
rowRef = ['language','title','QID',pValues[0][0],pValues[0][1],pValues[1][0],pValues[1][1],'accept value','Reference Link', 'context']
rowHuman = ['language','title','QID',pValues[0][0],pValues[0][1],pValues[1][0],pValues[1][1],'WP first sentence']
rowQS = ['QID of person', pValues[1][0], 'QID of '+pValues[1][1], 'stated in', 'enwiki']
rowEdit = ['language','title','QID',pValues[0][0],pValues[0][1],pValues[1][0],'popular','accept value',pValues[1][1],pValues[1][1]+' description','alt '+pValues[1][1],'WP first sentence']
rowQSallWP = ['QID','property id','property QID','referenced in','wikipediaQID']
rowQSRef = ['title','QID','property id','property value','property QID', 'stated in', 'refLink', 'context']
