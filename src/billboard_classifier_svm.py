import random
import collections
from util import *
import os
import textblob
import re
import math
import sys

#from senti_classifier import senti_classifier
#from textblob import Textblob

profanity = set(['fuck', 'shit', 'damn', 'bitch', 'fucked', 'nigga', 'ass', 'bastard', 'motherfucker', 'shit'])
cities = set(['los', 'angeles', 'la', 'new york', 'atlanta', 'atl', 'houston', 'chicago'])
brands = set(['nike', 'adidas', 'henny', 'hennessy', 'jordans', 'gucci', 'versace', 'prada', 'ralph', 'chanel', 'mercedes', 'patron', 'bentley'])

"""def featureExtractor(x):
	d = collections.defaultdict(float)
	firstLine = x.split('\n', 1)[0]
	lineSplit = x.split(':')
	title = lineSplit[0]
	artist = lineSplit[1]
	d[artist] = 1
	d = collections.defaultdict(int)
	words = x.split(' ')
	uniqueWords = set([])
	i = 0
	lastWordLine = ''
	for word in words:
		if (i == 0):
			#print(i)
			#sentiment score
			d['sentiment'] = float(word)
			i = i+1
			continue #trying to get sentiment
		#uniqueWords.add(word)
		#word = word.lower()
		#d[artist + ' ' + word] = 1
		if word in profanity or word in cities or word in brands:
			d[word] += 5
		i += 1
		if word[-1:] == '\n':
			word = re.sub("[^a-zA-Z]+", '', word)
			
			if lastWordLine[-1:] == word[-1:]:
				#print(word)
				#print(lastWordLine)
				d['lastRhyme'] += 1
			lastWordLine = word
	if i < 100:
		d['short'] = 1 #kinda wack for the actual thing made it worse
	elif 100 <= i and i < 200:
		d['medium'] = 1
	elif 200 <= i and i < 300:
		d['smedium'] = 1
	elif 300 <= i and i < 400:
		d['large'] = 1
	else:
		d['xtra'] = 1
	d['ratio_score'] = float(len(uniqueWords)) / float(len(words))
	return d"""


def featureExtractor(x):
	d = collections.defaultdict(float)
	i = 0 
	words = x.split(' ')
	uniqueWords = set([])
	firstLine = x.split('\n', 1)[0]
	lineSplit = x.split(':')
	title = lineSplit[0]
	artist = lineSplit[1]
	#d[artist] = 1
	artists = artist.split()
	for artist in artists:
		d[artist] = 1
		artistFeat = re.sub("[^a-zA-Z]+", '', artist)
		if artistFeat.lower() == 'feat' or artistFeat.lower() == 'featuring':
			d['feat__'] += 10
	lastWordLine = ''
	j = 0
	for word in words:
		#test
		#look for keywords like hook or chorus
		if (j == 0):
			d['sentiment_score'] = float(word)

			#print(i)
			#sentiment score
		#	d[word] = 1
		#	d[artist + ' ' + word] = 1
			j = j+1
			continue #trying to get sentiment	
		#word = re.sub("[^a-zA-Z]+", '', word).lower() #tried standardizing all words, but it made it worse
		uniqueWords.add(word)
		if word in profanity or word in cities or word in brands:
			d[word] += 10

		if word[-1:] == '\n':
			word = re.sub("[^a-zA-Z]+", '', word) #takes off the \n
			
			if lastWordLine[-2:] == word[-2:]:
				#print(word)
				#print(lastWordLine)
				d['lastRhyme'] += 1
			lastWordLine = word
		d[word] += 1 #unigram
		#d[artist + ' ' + word] += 1
		if i < len(words) - 1:
			nextWord = words[i + 2]


			#nextWord = re.sub("[^a-zA-Z]+", '', nextWord).lower() 
			d[word + ' ' + nextWord] += 1 #bigram
			#d[artist + ' ' + word + ' ' + nextWord] += 1
			if i < len(words) - 2:
				d[word + ' ' + nextWord + ' ' + words[i+3]] += 1 #trigram
		j += 1
		#i = i + 1
		#print(i)
	#if (float(len(uniqueWords)) / float(len(words)) ) > .4: #unique word ratio
	#	d['ratio_score'] = 1
		#d[artist + 'ratio_score'] = 1
		#print(float(len(uniqueWords)) / float(len(words)))

		#if word in profanity:
		#	d[word] = 1
		#d[word] = d[word] + 1

	return d

"""def featureExtractor(x):
	d = collections.defaultdict(int)
	i = 0 
	words = x.split()
	uniqueWords = set([])
	for word in words:
		#test
		#if (i == 0):
			#print(i)
			#sentiment score
		#	d[word] = 1
		#	d[artist + ' ' + word] = 1
		#	i = i+1
		#	continue #trying to get sentiment	
		#word = re.sub("[^a-zA-Z]+", '', word).lower() #tried standardizing all words, but it made it worse
		uniqueWords.add(word)
		d[word] += 1 #unigram
		#d[artist + ' ' + word] += 1
		if i < len(words) - 1:
			nextWord = words[i + 1]


			#nextWord = re.sub("[^a-zA-Z]+", '', nextWord).lower() 
			d[word + ' ' + nextWord] += 1 #bigram
			#d[artist + ' ' + word + ' ' + nextWord] += 1
			if i < len(words) - 2:
				d[word + ' ' + nextWord + ' ' + words[i+2]] += 1 #trigram
		#i = i + 1
		#print(i)
	if (float(len(uniqueWords)) / float(len(words)) ) > .4: #unique word ratio
		d['ratio_score'] = 1 
	#d['ratio_score'] = float(len(uniqueWords)) / float(len(words))
		#d[artist + 'ratio_score'] = 1
		#print(float(len(uniqueWords)) / float(len(words)))

		#if word in profanity:
		#	d[word] = 1
		#d[word] = d[word] + 1

	return d"""

def predictor(x, weights):
	score = 0
	features = featureExtractor(x)
	score = dotProduct(features, weights)
	#print score
	if score <= 0:
		return -1
	else:
		return 1

def learnPredictor(trainExamples, numIters, eta):
	weights = collections.defaultdict(int)
	lam = .5
	for j in xrange(numIters):
		eta = float(1) / math.sqrt(j + 1)
		for i in xrange(len(trainExamples)):
			x = trainExamples[i][0]
			y = trainExamples[i][1]
			features = featureExtractor(x)
			margin = y*dotProduct(weights, features)
			if margin < 1:
				for k2, v2 in features.iteritems():
					lossHinge = -(v2*y)
					weights[k2] = weights[k2] - (eta*(lossHinge+(lam * weights[k2]))) #im doing this on grad of loss not training loss and notes say training 

	#print weights
	return weights

def addPosOrNeg(songString):
	#posScore, negScore = senti_classifier.polarity_scores([songString])
	songBlob = textblob.TextBlob(songString)
	sentiment = songBlob.sentiment.polarity
	#print(sentiment)
	#if sentiment > 0.0:
	#if posScore > negScore:
	#	songString = 'positive_score ' + songString
	#else:
	#	songString = 'negative_score ' + songString
	songString = str(sentiment) + ' ' + songString
	return songString

def removeUnallowedMetadata(song):
	firstLine = song.split('\n', 1)[0]
	indicesOfColon = [s.start() for s in re.finditer(':', firstLine)]
	if len(indicesOfColon) > 1:
		firstLine = firstLine[:indicesOfColon[1]] 
	song = firstLine + ' ' + song[song.find('\n'):]
	return song

def labelTrainingExamples():
	inBillboardDirectory = '../lyrics/billboard-lyrics/training-set'
	trainingExamples = []
	for filename in os.listdir(inBillboardDirectory):
		song = ''
		if filename != '.DS_Store':
			with open(inBillboardDirectory + '/' + filename, 'r') as f:
				song = f.readlines()
				songString = ' '.join(song)
				songString = removeUnallowedMetadata(songString)
				#print("ERROR in billboard " + filename)
				
				songString = addPosOrNeg(songString)
				#songString = songString.replace('\n', '')
				#songString = songString.replace('\r', '')

				songEntry = (songString, 1)
				trainingExamples.append(songEntry)

	outOfBillboardDirectory = '../lyrics/non-billboard-lyrics/training-set'
	for filename in os.listdir(outOfBillboardDirectory):
		song = ''
		if filename != '.DS_Store':
			with open(outOfBillboardDirectory + '/' + filename, 'r') as f:
				song = f.readlines()
				songString = ' '.join(song)
				#print("ERROR not in billboard " + filename)
				
				songString = addPosOrNeg(songString)
				#songString = songString.replace('\n', '')
				#songString = songString.replace('\r', '')
				songEntry = (songString, -1)
				trainingExamples.append(songEntry)
	return trainingExamples



def labelTestExamples():
	inBillboardDirectory = '../lyrics/billboard-lyrics/validation-set'
	testExamples = []
	for filename in os.listdir(inBillboardDirectory):
		song = ''
		if filename != '.DS_Store':
			with open(inBillboardDirectory + '/' + filename, 'r') as f:
				song = f.readlines()
				songString = ' '.join(song)
				songString = removeUnallowedMetadata(songString)
				songString = addPosOrNeg(songString)
				#songString = songString.replace('\n', '')
				#songString = songString.replace('\r', '')
				songEntry = (songString, 1)
				testExamples.append(songEntry)

	outOfBillboardDirectory = '../lyrics/non-billboard-lyrics/validation-set'
	for filename in os.listdir(outOfBillboardDirectory):
		song = ''
		if filename != '.DS_Store':
			with open(outOfBillboardDirectory + '/' + filename, 'r') as f:
				song = f.readlines()
				songString = ' '.join(song)
				
				songString = addPosOrNeg(songString)
				#songString = songString.replace('\n', '')
				#songString = songString.replace('\r', '')
				songEntry = (songString, -1)
				testExamples.append(songEntry)
	return testExamples

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')


	trainingExamples = labelTrainingExamples()
	numIters = 500
	eta = .01

	weights = learnPredictor(trainingExamples, numIters, eta)

	testExamples = labelTestExamples()

	totalTested = len(testExamples)
	correct = 0
	tp = 0
	fp = 0 
	fn = 0 
	tn = 0
	for testExample in testExamples:
		prediction = predictor(testExample[0], weights)
		actual = testExample[1]
		if actual == 1 and prediction == 1:
			tp += 1
		if prediction == 1 and actual == -1:
			fp += 1
		if prediction == -1 and actual == 1:
			fn += 1
		if (actual == prediction):
			correct += 1
	percentageCorrect = float(correct) / float(totalTested)
	print "Accuracy: " + str(percentageCorrect)
	print "Precision: " + str(float(tp)/ (float(tp) + float(fp)))
	print "Recall: " + str(float(tp)/ (float(tp) + float(fn)))
if __name__ == "__main__":
	main()