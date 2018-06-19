from settings import *

# Variables only for quicksheets.py
inputFileNameQuickSheets = 'testList'
pValues = genderPValues.append(['P172','ethnic group'])
pValues = genderPValues
genderSelect = ["male","female","transgender female","transgender male","non-binary","intersex","transgender","hermaphrodite","neutral sex"] #choose from 'female', 'male', etc.
# If you want to use categories edit the following field ########################
useCategories = True
matrixName = '_QID_matrix_output_mar23.csv'
grep = True
matrixGrepName = '_QID_matrixGREP_output_mar23.csv'

# If you want to use the WP first sentence edit the following field ##############
useFirstSentence = True

# Variables both for quicksheets.py and quick-statement.py ##############
pValueListName = 'pList'
debug = False
getReferences = True
refLinkLimit = 5

# Variables only for quick-statement.py #####################################
nonWikiRef = getReferences
inputFileNameQuickStatements = 'output-references'
#Alex Pearlstein, Q19592455, P106, Video Artist, Q18216771, P248, http://artsatl.com/review-19/, Review: At Contemporary, video artist Alix Pearlstein leaves the ordinary

#don't edit below here
rowRef = ['language','title','QID',pValues[0][0],pValues[0][1],pValues[1][0],pValues[1][1],'accept value','Reference Link', 'context']
rowHuman = ['language','title','QID',pValues[0][0],pValues[0][1],pValues[1][0],pValues[1][1],'WP first sentence']
rowQS = ['QID of person', pValues[1][0], 'QID of '+pValues[1][1], 'stated in', 'enwiki']
rowEdit = ['language','title','QID',pValues[0][0],pValues[0][1],pValues[1][0],'popular','accept value',pValues[1][1],pValues[1][1]+' description','alt '+pValues[1][1],'WP first sentence']
rowQSallWP = ['QID','property id','property QID','referenced in','wikipediaQID']
rowQSRef = ['title','QID','property id','property value','property QID', 'stated in', 'refLink', 'context']
