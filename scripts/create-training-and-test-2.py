#This dataset (#2) will resample billboard songs, and non-billboard songs will come from non-billboard artists
#The size of the dataset will be the same as in dataset (#1)

import os, random
#1509 non
#1324 billboard

numOfValidationOrTestFilesNon = 151
numOfValidationOrTestFilesBillboard = 133
numOfTrainingFilesNon = 1208

billboardDirectory = '../lyrics/all-billboard'
nonBillboardDirectory = '../lyrics/all-non-billboard-artist'


billboardDirectoryDestination = '../lyrics/dataset_2/billboard-lyrics'
nonBillboardDirectoryDestination = '../lyrics/dataset_2/non-billboard-lyrics'

#Billboard
for i in range(numOfValidationOrTestFilesBillboard):
  choosenFile = random.choice(os.listdir(billboardDirectory))
	#move file to test folder
  if choosenFile.endswith(".txt"):
    print (billboardDirectory + '/' + choosenFile, billboardDirectoryDestination + '/test-set/' + choosenFile)
    os.rename(billboardDirectory + '/' + choosenFile, billboardDirectoryDestination + '/test-set/' + choosenFile)
for j in range(numOfValidationOrTestFilesBillboard):
  choosenFile = random.choice(os.listdir(billboardDirectory))
  if choosenFile.endswith(".txt"):
    os.rename(billboardDirectory + '/' + choosenFile, billboardDirectoryDestination + '/validation-set/' + choosenFile)
for filename in os.listdir(billboardDirectory):
  if filename.endswith(".txt"):
    os.rename(billboardDirectory + '/' + filename, billboardDirectoryDestination + '/training-set/' + filename)

print ('Done with billboard...')

nonbillboard
for i in xrange(numOfValidationOrTestFilesNon):
  choosenFile = random.choice(os.listdir(nonBillboardDirectory))
	#move file to test folder
  if choosenFile.endswith(".txt"):
    os.rename(nonBillboardDirectory + '/' + choosenFile, nonBillboardDirectoryDestination + '/test-set/' + choosenFile)
for j in xrange(numOfValidationOrTestFilesNon):
  choosenFile = random.choice(os.listdir(nonBillboardDirectory))
  if choosenFile.endswith(".txt"):
    os.rename(nonBillboardDirectory + '/' + choosenFile, nonBillboardDirectoryDestination + '/validation-set/' + choosenFile)
for k in xrange(numOfTrainingFilesNon):
  choosenFile = random.choice(os.listdir(nonBillboardDirectory))

  if choosenFile.endswith(".txt"):
    os.rename(nonBillboardDirectory + '/' + choosenFile, nonBillboardDirectoryDestination + '/training-set/' + choosenFile)

print ('Done')