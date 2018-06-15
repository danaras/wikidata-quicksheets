# Variables both for quicksheets.py and quick-statement.py ##############
pValueListName = 'pList'
debug = False
getReferences = True
rowQS = ['QID of person', pValues[1][0], 'QID of '+pValues[1][1], 'stated in', 'enwiki']
rowEdit = ['language','title','QID',pValues[0][0],pValues[0][1],pValues[1][0],'popular','accept value',pValues[1][1],pValues[1][1]+' description','alt '+pValues[1][1],'WP first sentence']
firstline = True

# Variables only for quicksheets.py
inputFileNameQuickSheets = 'testList'
pValues = [['P21','gender'],['P172','ethnic group']]
genderSelect = ["male","female","transgender female","transgender male","non-binary","intersex","transgender","hermaphrodite","neutral sex"] #choose from 'female', 'male', etc.

useCategories = False
matrixName = '_QID_matrix_output_mar23.csv'
grep = True
matrixGrepName = '_QID_matrixGREP_output_mar23.csv'

useFirstSentence = False
firstSentence = ''

refLinkLimit = 5
rowRef = ['language','title','QID',pValues[0][0],pValues[0][1],pValues[1][0],pValues[1][1],'accept value','Reference Link', 'context']

rowHuman = ['language','title','QID',pValues[0][0],pValues[0][1],pValues[1][0],pValues[1][1],'WP first sentence']

title =''
language =''
qid=''
entitiesFound = False

# Variables only for quick-statement.py #####################################
nonWikiRef = True
inputFileNameQuickStatements = 'output-references'
rowQSallWP = ['QID','property id','occupationQID','referenced in','wikipediaQID']
rowQSRef = []
wpEn = "Q328"
wikipediaQID = ''
referencedIn = "S143"
propertyId = "P106"
