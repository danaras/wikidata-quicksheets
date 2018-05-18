rowEdit = ['language','title','QID','p21','gender','p106','popular','accept value','occupation','occupation description','alt occupation','pw first sentence']
rowHuman = ['language','title','QID','p21','gender','p106','occupation','pw first sentence']
rowQS = ['QID of person', 'P106', 'QID of occupation', 'stated in', 'enwiki']

inputFileName = 'output-drafts'
matrixName = '_QID_matrix_output_mar23.csv'
matrixGrepName = '_QID_matrixGREP_output_mar23.csv'
grep = True
title =''
language =''
qid=''
entitiesFound = False
firstSentence = ''
p21 = ''
p106 = ''
gender = ''
occupation = ''
firstline = True
