import os, random
#1509 non
#1324 billboard
numOfValidationOrTestFilesNon = 151
numOfValidationOrTestFilesBillboard = 133
billboardDirectory = 'lyrics/billboard-lyrics'
nonBillboardDirectory = 'lyrics/non-billboard-lyrics'
#Billboard
for i in xrange(numOfValidationOrTestFilesBillboard):
	choosenFile = random.choice(os.listdir(billboardDirectory))
	#move file to test folder
	if choosenFile.endswith(".txt"):
		os.rename(billboardDirectory + '/' + choosenFile, billboardDirectory + '/test-set/' + choosenFile)
for j in xrange(numOfValidationOrTestFilesBillboard):
	choosenFile = random.choice(os.listdir(billboardDirectory))
	if choosenFile.endswith(".txt"):
		os.rename(billboardDirectory + '/' + choosenFile, billboardDirectory + '/validation-set/' + choosenFile)
for filename in os.listdir(billboardDirectory):
	if filename.endswith(".txt"):
		os.rename(billboardDirectory + '/' + filename, billboardDirectory + '/training-set/' + filename)

#nonbillboard
for i in xrange(numOfValidationOrTestFilesNon):
	choosenFile = random.choice(os.listdir(nonBillboardDirectory))
	#move file to test folder
	if choosenFile.endswith(".txt"):
		os.rename(nonBillboardDirectory + '/' + choosenFile, nonBillboardDirectory + '/test-set/' + choosenFile)
for j in xrange(numOfValidationOrTestFilesNon):
	choosenFile = random.choice(os.listdir(nonBillboardDirectory))
	if choosenFile.endswith(".txt"):
		os.rename(nonBillboardDirectory + '/' + choosenFile, nonBillboardDirectory + '/validation-set/' + choosenFile)
for filename in os.listdir(nonBillboardDirectory):
	if filename.endswith(".txt"):
		os.rename(nonBillboardDirectory + '/' + filename, nonBillboardDirectory + '/training-set/' + filename)