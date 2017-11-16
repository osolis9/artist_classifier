import random
import collections
from util import *
import os

def predictor(x, weights):
	score = 0
	features = featureExtractor(x)
	score = dotProduct(features, weights)
	if score <= 0:
		return -1
	else:
		return 1

def featureExtractor(x):
	d = collections.defaultdict(int)
	for word in x.split():
		d[word] = d[word] + 1
	return d

def learnPredictor(trainExamples, numIters, eta):
	weights = collections.defaultdict(int)
	for i in xrange(numIters):
		for i in xrange(len(trainExamples)):
			x = trainExamples[i][0]
			y = trainExamples[i][1]
			features = featureExtractor(x)
			margin = y*dotProduct(weights, features)
			if margin < 1:
				for k2, v2 in features.iteritems():
					lossHinge = -(v2*y)
					weights[k2] = weights[k2] - (eta*lossHinge)

	return weights

def labelTrainingExamples():
	inBillboardDirectory = '../lyrics/billboard-lyrics/training-set'
	trainingExamples = []
	for filename in os.listdir(inBillboardDirectory):
		song = ''
		if filename != '.DS_Store':
			with open(inBillboardDirectory + '/' + filename, 'r') as f:
				song = f.readlines()
				songString = ' '.join(song)
				songString = songString.replace('\n', '')
				songString = songString.replace('\r', '')
				songEntry = (songString, 1)
				trainingExamples.append(songEntry)

	outOfBillboardDirectory = '../lyrics/non-billboard-lyrics/training-set'
	for filename in os.listdir(outOfBillboardDirectory):
		song = ''
		with open(outOfBillboardDirectory + '/' + filename, 'r') as f:
				song = f.readlines()
				songString = ' '.join(song)
				songString = songString.replace('\n', '')
				songString = songString.replace('\r', '')
				songEntry = (songString, -1)
				trainingExamples.append(songEntry)
	return trainingExamples

def labelTestExamples():
	inBillboardDirectory = '../lyrics/billboard-lyrics/test-set'
	testExamples = []
	for filename in os.listdir(inBillboardDirectory):
		song = ''
		with open(inBillboardDirectory + '/' + filename, 'r') as f:
				song = f.readlines()
				songString = ' '.join(song)
				songString = songString.replace('\n', '')
				songString = songString.replace('\r', '')
				songEntry = (songString, 1)
				testExamples.append(songEntry)

	outOfBillboardDirectory = '../lyrics/non-billboard-lyrics/test-set'
	for filename in os.listdir(outOfBillboardDirectory):
		song = ''
		with open(outOfBillboardDirectory + '/' + filename, 'r') as f:
				song = f.readlines()
				songString = ' '.join(song)
				songString = songString.replace('\n', '')
				songString = songString.replace('\r', '')
				songEntry = (songString, -1)
				testExamples.append(songEntry)
	return testExamples

def main():
	trainingExamples = labelTrainingExamples()
	numIters = 1
	eta = .01
	weights = learnPredictor(trainingExamples, numIters, eta)
	for key, value in weights.iteritems():
		print key
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

if __name__ == "__main__":
	main()