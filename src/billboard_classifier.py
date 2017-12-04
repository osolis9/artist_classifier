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
import json

#Can add to profanity list
profanity = set(['fuck', 'shit', 'damn', 'bitch', 'fucked', 'nigga', 'ass', 'bastard', 'motherfucker', 'shit'])

cities = set(['los', 'angeles', 'la', 'new york', 'atlanta', 'atl', 'houston', 'chicago'])
brands = set(['nike', 'adidas', 'henny', 'hennessy', 'jordans', 'gucci', 'versace', 'prada', 'ralph', 'chanel', 'mercedes', 'patron', 'bentley'])

json_song_themes = open('../song_info/song_themes.json').read()
song_themes = json.loads(json_song_themes)

# Returns (title, artist, sentiment, words) tuple
def parseLyrics(x):
	lines = x.split('\n', 1)
	firstLine = lines[0]

	rest = lines[1]

	song_theme_key = firstLine.split(' ', 1)[1]

	#To make weird features work,
	#need words = x.split() here
	# words = x.split()
	words = rest.split()

	firstLineSplit = firstLine.split(':')
	artist = firstLineSplit[1]
	firstHalfSplit = firstLineSplit[0].split(' ', 1)
	sentiment = float(firstHalfSplit[0])
	title = firstHalfSplit[1].replace('-', ' ')
	return (title, artist, sentiment, song_theme_key.strip(), words)


def featureExtractor(x):
	d = collections.defaultdict(float)
	i = 0

	title, artist, sentiment, song_theme_key, words = parseLyrics(x)
	uniqueWords = set([])

	if song_theme_key not in song_themes:
		song_theme_key = song_theme_key + ' '
	p = song_themes[song_theme_key]
	d['Crime'] 											= p['Crime']
	d['Death'] 											= p['Death']
	d['Disabled'] 									= p['Disabled']
	d['Ethnicity'] 									= p['Ethnicity']
	d['Folklore'] 									= p['Folklore']
	d['Future'] 										= p['Future']
	d['Genealogy'] 									= p['Genealogy']
	d['Government'] 								= p['Government']
	d['History'] 										= p['History']
	d['Holidays'] 									= p['Holidays']
	d['Law'] 												= p['Law']
	d['Lifestyle_Choices'] 					= p['Lifestyle_Choices']
	d['Military'] 									= p['Military']
	d['Organizations'] 							= p['Organizations']
	d['Paranormal']									= p['Paranormal']
	d['Philanthropy'] 							= p['Philanthropy']
	d['Philosophy'] 								= p['Philosophy']
	d['Politics'] 									= p['Politics']
	d['Relationships'] 							= p['Relationships']
	d['Religion_and_Spirituality'] 	= p['Religion_and_Spirituality']
	d['Sexuality'] 									= p['Sexuality']
	d['Subcultures'] 								= p['Subcultures']
	d['Support_Groups'] 						= p['Support_Groups']
	d['Transgendered']	 						= p['Transgendered']
	d['Work'] 											= p['Work']

	#Sentiment
	#Positive/Negative?
	d['sentiment_score'] = sentiment

	titleLength = len(title.split())
	if titleLength > 6:
		d['long_title'] = 1

	artists = artist.split()
	for artist in artists:
		#This seems like it would be cheating
		#d[artist] = 1
		artistFeat = re.sub("[^a-zA-Z]+", '', artist)
		artistFeat = artistFeat.lower()

		#Featured artists (which one is better here?)
		if artistFeat.startswith('feat') or artistFeat.startswith('ft.'):
			d['featured_artists'] += 10
			#d['featured_artists'] = 1

	#Remix, Acoustic, Interlude
	for word in title.split():
		if word == 'remix' or word == 'acoustic' or word == 'interlude':
			d['remix'] = 1


	lastWordLine = ''
	j = 0
	#look for keywords like hook or chorus
	for word in words:
		uniqueWords.add(word)
		if word in profanity or word in cities or word in brands:
			d[word] += 10

		if word[-1:] == '\n':
			word = re.sub("[^a-zA-Z]+", '', word) #takes off the \n
			if lastWordLine[-2:] == word[-2:]:
				d['lastRhyme'] += 1
			lastWordLine = word


		#Weird feature stuff. Can be uncommented for large boost, still need to figure out how this works

		#d[word] += 1 #unigram
		# d[artist + ' ' + word] += 1
		# if i < len(words) - 1:
		# 	nextWord = words[i + 2]
		# 	nextWord = re.sub("[^a-zA-Z]+", '', nextWord).lower()
		# 	d[word + ' ' + nextWord] += 1 #bigram
		# 	d[artist + ' ' + word + ' ' + nextWord] += 1
		# 	if i < len(words) - 2:
		# 		d[word + ' ' + nextWord + ' ' + words[i+3]] += 1 #trigram
		# j += 1


	# Ratio for repetition
	d['ratio_score'] = float(len(uniqueWords)) / float(len(words))

	# Number of words buckets
	numWords = len(words)
	if numWords < 200:
		d['words_200'] = 1
	elif numWords > 200 and numWords <= 400:
		d['words_200-400'] = 1
	elif numWords > 400 and numWords <= 600:
		d['words_400-600'] = 1
	elif numWords > 600 and numWords <= 800:
		d['words_600-800'] = 1
	elif numWords > 800 and numWords <= 1000:
		d['words_800-1000'] = 1
	elif numWords > 1000 and numWords <= 1200:
		d['words_1000-1200'] = 1
	elif numWords > 1200 and numWords <= 1400:
		d['words_1200-1400'] = 1
	else:
		d['words_1400'] = 1

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

	print (weights)
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

	print (weights)
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
	parser.add_argument("--e", help="eta value, .01 by default", type=float)
	parser.add_argument("--d", help="dataset to use, dataset_1 by default")
	args = parser.parse_args()

	valid_datasets = ['dataset_1', 'dataset_2']
	dataset = ''
	if args.d and args.d in valid_datasets:
		dataset = args.d
	else:
		dataset = 'dataset_1'


	trainingExamples = labelTrainingExamples(dataset)

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


	testExamples = labelTestExamples(dataset)
	evaluatePredictor(testExamples, weights, predictor)

if __name__ == "__main__":
	main(sys.argv[1:])