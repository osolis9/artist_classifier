import os, random

numOfTestFiles = 160
numOfValidationFiles = 144
billboardDirectory = 'lyrics/billboard-lyrics'
nonBillboardDirectory = 'lyrics/non-billboard-lyrics'
for i in xrange(numOfTestFiles):
	choosenFile = random.choice(os.listdir(billboardDirectory))
	#move file to test folder
	if choosenFile.endswith(".txt"):
		os.rename(billboardDirectory + '/' + choosenFile, billboardDirectory + '/test-set/' + choosenFile)
for j in xrange(numOfValidationFiles):
	choosenFile = random.choice(os.listdir(billboardDirectory))
	if choosenFile.endswith(".txt"):
		os.rename(billboardDirectory + '/' + choosenFile, billboardDirectory + '/validation-set/' + choosenFile)
for filename in os.listdir(billboardDirectory):
	if filename.endswith(".txt"):
		os.rename(billboardDirectory + '/' + filename, billboardDirectory + '/training-set/' + filename)

for i in xrange(numOfTestFiles):
	choosenFile = random.choice(os.listdir(nonBillboardDirectory))
	#move file to test folder
	if choosenFile.endswith(".txt"):
		os.rename(nonBillboardDirectory + '/' + choosenFile, nonBillboardDirectory + '/test-set/' + choosenFile)
for j in xrange(numOfValidationFiles):
	choosenFile = random.choice(os.listdir(nonBillboardDirectory))
	if choosenFile.endswith(".txt"):
		os.rename(nonBillboardDirectory + '/' + choosenFile, nonBillboardDirectory + '/validation-set/' + choosenFile)
for filename in os.listdir(nonBillboardDirectory):
	if filename.endswith(".txt"):
		os.rename(nonBillboardDirectory + '/' + filename, nonBillboardDirectory + '/training-set/' + filename)