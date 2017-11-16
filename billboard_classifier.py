import random
import collections
from util import *
import os


def predictor(x, weights):
    score = 0
    features = featureExtractor(x)
    score = util.dotProduct(features, weights)
    if score <= 0:
        return 1
    else:
        return -1

def featureExtractor(x):
	d = collections.defauldict(int)
	for word in words:
		d[word] = d[word] + 1
	return d

def learnPredictor(trainExamples, numIters, eta):
	weights = collections.defauldict(int)
	for i in xrange(numIters):
        for i in xrange(len(trainExamples)):
        	x = trainExamples[i][0]
        	y = trainExamples[i][1]
        	features = featureExtractor(x)
        	margin = y*util.dotProduct(weights, features)
        	if margin < 1:
        		for k2, v2 in features.iteritems():
        			lossHinge = -(v2*y) 
        			weights[k2] = weights[k2] - (eta*lossHinge)

	return weights

def labelTrainingExamples():
	inBillboardDirectory = 'billboard-lyrics/training-examples'
	trainingexamples = []
	for filename in os.listdir(inBillboardDirectory):
		song = ''
		with open(inBillboardDirectory + '/' filename, 'r') as f:
			song = f.readlines()
		songEntry = (song, 1)
		trainingExamples.append(songEntry)

	outOfBillboardDirectory = 'non-billboard-lyrics/training-examples'
	for filename in os.listdir(outOfBillboardDirectory):
		song = ''
		with open(outOfBillboardDirectory + '/' filename, 'r') as f:
			song = f.readlines()
		songEntry = (song, -1)
		trainingExamples.append(songEntry)
	return trainingExamples

def labelTestExamples():
	inBillboardDirectory = 'billboard-lyrics/test-examples'
	testExamples = []
	for filename in os.listdir(inBillboardDirectory):
		song = ''
		with open(inBillboardDirectory + '/' filename, 'r') as f:
			song = f.readlines()
		songEntry = (song, 1)
		testExamples.append(songEntry)

	outOfBillboardDirectory = 'non-billboard-lyrics/test-examples'
	for filename in os.listdir(outOfBillboardDirectory):
		song = ''
		with open(outOfBillboardDirectory + '/' filename, 'r') as f:
			song = f.readlines()
		songEntry = (song, -1)
		testExamples.append(songEntry)
	return testExamples

def main():
	trainingExamples = labelTrainingExamples()
	numIters = 100
	eta = .01
	weights = learnPredictor(trainingExamples, numIters, eta)
	testExamples = labelTestExamples()
	totalTested = len(testExamples)
	correct = 0
	for testExample in testExamples:
		prediction = predictor(testExample[0], weights)
		actual = testExample[1]
		if (actual == prediction):
			correct += 1
	percentageCorrect = float(correct) / float(totalTested)

	print "Ratio Classified Correctly: " + str(percentageCorrect)
	#read all trainingexamples and label with a 1 or -1 and put in a list
	#call learn predictor on training examples
	#see how well it did

if __name__ "__main__":
	main()