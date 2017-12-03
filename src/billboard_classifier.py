import random
import collections
from util import *
import os
import re
import sys
from importlib import reload
import getopt
import math
import argparse

featurePrefixes = ['feat', 'ft.']

profanity = set(['fuck', 'shit', 'damn', 'bitch', 'fucked', 'nigga', 'ass', 'bastard', 'motherfucker', 'shit'])
cities = set(['los', 'angeles', 'la', 'new york', 'atlanta', 'atl', 'houston', 'chicago'])
brands = set(['nike', 'adidas', 'henny', 'hennessy', 'jordans', 'gucci', 'versace', 'prada', 'ralph', 'chanel', 'mercedes', 'patron', 'bentley'])


"""def featureExtractor(x):



	d = collections.defaultdict(int)
	i = 0

	# split out first line
	# get information from first line
	# features on title and author
	lines = x.split('\n', 1)
	firstLine = lines[0]
	rest = lines[1]

	# firstLineSplit = firstLine.split(':')
	# title = firstLineSplit[0]
	# title = title.replace('-', ' ')
	# artist = firstLineSplit[1]

	# print (title)
	# print (artist)

	# #FEATURED ARTISTS
	# #startsWith instead of in
	# #'with' for artists
	# for word in title:
	# 	for featurePrefix in featurePrefixes:
	# 		if featurePrefix in word.lower():
	# 			d['featured_artist'] = 1
	# 			print ('got here')
	# 		if 'remix' in word.lower():
	# 			d['remix'] = 1
	# 			print ('got here')
	# for word in artist:
	# 	for featurePrefix in featurePrefixes:
	# 		if featurePrefix in word.lower():
	# 			d['featured_artist'] = 1
	# 			print ('got here')

	# print (title)
	# print (artist)
	# print ('')
	# print ('')

	#Buckets
	#d['titleLength'] = len(title)

	# Featuring
	# Remix

	words = rest.split()
	#words = x.split()


	uniqueWords = set([])
	for word in words:
		uniqueWords.add(word)
		d[word] += 1 #unigram
		#d[artist + ' ' + word] += 1
		if i < len(words) - 1:
			nextWord = words[i + 1]


			#nextWord = re.sub("[^a-zA-Z]+", '', nextWord).lower()

			#uncomment
			d[word + ' ' + nextWord] += 1 #bigram

			#d[artist + ' ' + word + ' ' + nextWord] += 1
			if i < len(words) - 2:
				d[word + ' ' + nextWord + ' ' + words[i+2]] += 1 #trigram
		#i = i + 1
		#print(i)
	#if (float(len(uniqueWords)) / float(len(words)) ) > .4: #unique word ratio
	#	d['ratio_score'] = 1
	d['ratio_score'] = float(len(uniqueWords)) / float(len(words))
		#d[artist + 'ratio_score'] = 1
		#print(float(len(uniqueWords)) / float(len(words)))


	for swearPrefix in profanity:
		if swearPrefix in word:
			d['profanity'] += 1

	#i = i + 1


	d['ratio_score'] = float(len(uniqueWords)) / float(len(words))
	# numWords = len(words)
	# if numWords < 200:
	# 	d['words_200'] = 1
	# elif numWords > 200 and numWords <= 400:
	# 	d['words_200-400'] = 1
	# elif numWords > 400 and numWords <= 600:
	# 	d['words_400-600'] = 1
	# elif numWords > 600 and numWords <= 800:
	# 	d['words_600-800'] = 1
	# elif numWords > 800 and numWords <= 1000:
	# 	d['words_800-1000'] = 1
	# elif numWords > 1000 and numWords <= 1200:
	# 	d['words_1000-1200'] = 1
	# elif numWords > 1200 and numWords <= 1400:
	# 	d['words_1200-1400'] = 1
	# else:
	# 	d['words_1400'] = 1





		#test
		# if i == 0:
		# 	sentimentScore = float(word)
		# 	print(sentimentScore)
		# 	if sentimentScore > .5:
		# 		d['sentiment_score'] = 1
		# 	continue #trying to get sentiment
		#word = re.sub("[^a-zA-Z]+", '', word).lower() #tried standardizing all words, but it made it worse
		#nextWord = re.sub("[^a-zA-Z]+", '', nextWord).lower()
		#if word in profanity:
		#	d[word] = 1
		#d[word] = d[word] + 1

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


def predictor(x, weights):
	score = 0
	features = featureExtractor(x)
	score = dotProduct(features, weights)
	#print score
	if score <= 0:
		return -1
	else:
		return 1

def learnPredictorRegular(trainExamples, numIters, eta):
	weights = collections.defaultdict(int)
	for i in range(numIters):
		print ('Starting iteration ' + str(i) + '...')
		for i in range(len(trainExamples)):
			x = trainExamples[i][0]
			y = trainExamples[i][1]
			features = featureExtractor(x)
			margin = y*dotProduct(weights, features)
			if margin < 1:
				for k2, v2 in features.items():
					lossHinge = -(v2*y)
					weights[k2] = weights[k2] - (eta*lossHinge)

	#print weights
	return weights

def learnPredictorSVM(trainExamples, numIters, eta):
	weights = collections.defaultdict(int)
	lam = .5
	for j in range(numIters):
		print ('Starting iteration ' + str(j) + '...')
		eta = float(1) / math.sqrt(j + 1)
		for i in range(len(trainExamples)):
			x = trainExamples[i][0]
			y = trainExamples[i][1]
			features = featureExtractor(x)
			margin = y*dotProduct(weights, features)
			if margin < 1:
				for k2, v2 in features.items():
					lossHinge = -(v2*y)
					weights[k2] = weights[k2] - (eta*(lossHinge+(lam * weights[k2]))) #im doing this on grad of loss not training loss and notes say training

	#print weights
	return weights




# Arguments
# n - numIters
# e - eta
# d - data
# c - classifier to use

def main(argv):
	reload(sys)
	parser = argparse.ArgumentParser()
	parser.add_argument("--c", help="type of classifier, regular by default")
	parser.add_argument("--i", help="number of iterations, 50 by default", type=int)
	parser.add_argument("--e", help="eta value, .01 by default", type=int)
	args = parser.parse_args()

	trainingExamples = labelTrainingExamples()

	if args.i:
		numIters = args.i
	else:
		numIters = 50

	if args.e:
		eta = args.e
	else:
		eta = .01

	if args.c == 'svm':
		weights = learnPredictorSVM(trainingExamples, numIters, eta)
	elif args.c == 'regular':
		weights = learnPredictorRegular(trainingExamples, numIters, eta)
	else:
		weights = learnPredictorRegular(trainingExamples, numIters, eta)


	testExamples = labelTestExamples()
	evaluatePredictor(testExamples, weights, predictor)

if __name__ == "__main__":
	main(sys.argv[1:])