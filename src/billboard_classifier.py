import random
import collections
from util import *
import os
#import textblob
import re
#from indicoio import sentiment
#from textblob import Textblob

profanity = set(['fuck', 'shit', 'damn', 'bitch', 'fucked', 'nigga', 'ass', 'bastard', 'motherfucker', 'shit'])

def predictor(x, weights):
	score = 0
	features = featureExtractor(x)
	score = dotProduct(features, weights)
	#print score
	if score <= 0:
		return -1
	else:
		return 1

def featureExtractor(x):
	d = collections.defaultdict(int)
	i = 0 
	words = x.split()
	uniqueWords = set([])
	for word in words:
		"""if i == 0:
			sentimentScore = float(word)
			print(sentimentScore)
			if sentimentScore > .5:
				d['sentiment_score'] = 1
			continue""" #trying to get sentiment			
		#word = re.sub("[^a-zA-Z]+", '', word).lower() #tried standardizing all words, but it made it worse
		uniqueWords.add(word)
		d[word] += 1 #unigram
		
		if i < len(words) - 1:
			nextWord = words[i + 1]


			#nextWord = re.sub("[^a-zA-Z]+", '', nextWord).lower() 
			d[word + ' ' + nextWord] += 1 #bigram
			if i < len(words) - 2:
				d[word + ' ' + nextWord + ' ' + words[i+2]] += 1 #trigram
	if (float(len(uniqueWords)) / float(len(words)) ) > .3: #unique word ratio
		d['ratio_score'] = 1 

		#if word in profanity:
		#	d[word] = 1
		#d[word] = d[word] + 1
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

	#print weights
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
				#print songString
				#sentimentScore = sentiment(songString)
				#songString = str(sentimentScore) + ' ' + songString
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
				#sentimentScore = sentiment(songString)
				#songString = str(sentimentScore) + ' ' + songString
				songString = songString.replace('\n', '')
				songString = songString.replace('\r', '')
				songEntry = (songString, -1)
				trainingExamples.append(songEntry)
	return trainingExamples

def labelTestExamples():
	inBillboardDirectory = '../lyrics/billboard-lyrics/validation-set'
	testExamples = []
	for filename in os.listdir(inBillboardDirectory):
		song = ''
		with open(inBillboardDirectory + '/' + filename, 'r') as f:
				song = f.readlines()
				songString = ' '.join(song)
				#sentimentScore = sentiment(songString)
				#songString = str(sentimentScore) + ' ' + songString
				songString = songString.replace('\n', '')
				songString = songString.replace('\r', '')
				songEntry = (songString, 1)
				testExamples.append(songEntry)

	outOfBillboardDirectory = '../lyrics/non-billboard-lyrics/validation-set'
	for filename in os.listdir(outOfBillboardDirectory):
		song = ''
		with open(outOfBillboardDirectory + '/' + filename, 'r') as f:
				song = f.readlines()
				songString = ' '.join(song)
				#sentimentScore = sentiment(songString)
				#songString = str(sentimentScore) + ' ' + songString
				songString = songString.replace('\n', '')
				songString = songString.replace('\r', '')
				songEntry = (songString, -1)
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


if __name__ == "__main__":
	main()