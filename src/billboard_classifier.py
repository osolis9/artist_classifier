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
import decimal

#Can add to profanity list


cities = set(['los', 'angeles', 'la', 'new york', 'atlanta', 'atl', 'houston', 'chicago'])
brands = set(['nike', 'adidas', 'henny', 'hennessy', 'jordans', 'gucci', 'versace', 'prada', 'ralph', 'chanel', 'mercedes', 'patron', 'bentley'])
profanity = set(['fuck', 'shit', 'damn', 'bitch', 'fucked', 'nigga', 'ass', 'bastard', 'motherfucker'])

json_song_themes = open('../song_info/song_themes.json').read()
song_themes = json.loads(json_song_themes)


# IMPORTANT - This must be kept up to date with features for Naive Bayes to work in its current form...
feature_list = [
	'Crime',
	'Death',
	'Disabled',
	'Ethnicity',
	'Folklore',
	'Future',
	'Genealogy',
	'Government',
	'History',
	'Holidays',
	'Law',
	'Lifestyle_Choices',
	'Military',
	'Organizations',
	'Paranormal',
	'Philanthropy',
	'Philosophy',
	'Politics',
	'Relationships',
	'Religion_and_Spirituality',
	'Sexuality',
	'Subcultures',
	'Support_Groups',
	'Transgendered',
	'Work',
	'sentiment_score',
	'long_title',
	'featured_artists',
	'remix',
	'last_rhyme',
	'ratio_score',
	'words_200',
	'words_200-400',
	'words_400-600',
	'words_600-800',
	'words_800-1000',
	'words_1000-1200',
	'words_1200-1400',
	'words_1400',
]
feature_list = feature_list + list(profanity) + list(cities) + list(brands)


# Returns (title, artist, sentiment, words) tuple
def parseLyrics(x):
	lines = x.split('\n', 1)
	firstLine = lines[0]

	rest = lines[1]

	song_theme_key = firstLine.split(' ', 1)[1]

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
	if song_theme_key == '4:44  Let me tell you what I\'m dreaming of ':
		song_theme_key = '4:44'

	p = song_themes[song_theme_key]
	d['Crime'] 											= p['Crime']*1
	d['Death'] 											= p['Death']*1
	d['Disabled'] 									= p['Disabled']*1
	d['Ethnicity'] 									= p['Ethnicity']*1
	d['Folklore'] 									= p['Folklore']*1
	d['Future'] 										= p['Future']*1
	d['Genealogy'] 									= p['Genealogy']*1
	d['Government'] 								= p['Government']*1
	d['History'] 										= p['History']*1
	d['Holidays'] 									= p['Holidays']*1
	d['Law'] 												= p['Law']*1
	d['Lifestyle_Choices'] 					= p['Lifestyle_Choices']*1
	d['Military'] 									= p['Military']*1
	d['Organizations'] 							= p['Organizations']*1
	d['Paranormal']									= p['Paranormal']*1
	d['Philanthropy'] 							= p['Philanthropy']*1
	d['Philosophy'] 								= p['Philosophy']*1
	d['Politics'] 									= p['Politics']*1
	d['Relationships'] 							= p['Relationships']*1
	d['Religion_and_Spirituality'] 	= p['Religion_and_Spirituality']*1
	d['Sexuality'] 									= p['Sexuality']*1
	d['Subcultures'] 								= p['Subcultures']*1
	d['Support_Groups'] 						= p['Support_Groups']*1
	d['Transgendered']	 						= p['Transgendered']*1
	d['Work'] 											= p['Work']*1

	#Sentiment
	#Positive/Negative?
	d['sentiment_score'] = sentiment

	titleLength = len(title.split())
	if titleLength > 6:
		d['long_title'] = 1

	for titleWord in title.split():
		if titleWord.startswith('feat') or titleWord.startswith('ft.'):
			d['featured_artists'] = 1


	artists = artist.split()
	for artist in artists:
		#This seems like it would be cheating
		#artist = re.sub("[^a-zA-Z]+", '', artist).lower()
		#if not artist.startswith('feat') and not artist.startswith('ft.'):
		#	d[artist] = 1
		artistFeat = re.sub("[^a-zA-Z]+", '', artist)
		artistFeat = artistFeat.lower()

		#Featured artists (which one is better here?)
		if artistFeat.startswith('feat') or artistFeat.startswith('ft.'):
			d['featured_artists'] = 1
			#d['featured_artists'] = 1

	#Remix, Acoustic, Interlude
	for word in title.split():
		if word == 'remix' or word == 'acoustic' or word == 'interlude':
			d['remix'] = 1


	lastWordLine = ''
	j = 0
	#look for keywords like hook or chorus
	#good one
	for word in words:
		uniqueWords.add(word)
		# if word in profanity or word in cities or word in brands:
			# d[word] += 10

		if word[-1:] == '\n':
			word = re.sub("[^a-zA-Z]+", '', word) #takes off the \n
			if lastWordLine[-2:] == word[-2:]:
				d['last_rhyme'] += 1
			lastWordLine = word


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


def predictor(x, weights, classifier):
	score = 0
	features = featureExtractor(x)
	score = dotProduct(features, weights)
	print(score)
	if classifier == 'logistic':
		if score <= 0.5:
			return -1
		else:
			return 1
	else:
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

	printWeights(weights)
	return weights

def learnPredictorSVM(trainExamples, numIters, eta):
	weights = collections.defaultdict(int)
	lam = .01 #best results .1 gives an ok result
	for j in range(numIters):
		print ('Starting iteration ' + str(j) + '...')
		#eta = float(1) / math.sqrt(j + 1)
		for i in range(len(trainExamples)):
			x = trainExamples[i][0]
			y = trainExamples[i][1]
			features = featureExtractor(x)
			margin = y*dotProduct(weights, features)
			if margin < 1:
				for k2, v2 in features.items():
					lossHinge = -(v2*y)
					weights[k2] = weights[k2] - (eta*(lossHinge+(lam * weights[k2]))) #im doing this on grad of loss not training loss and notes say training

	printWeights(weights)
	return weights

def learnPredictorLogistic(trainExamples, numIters, eta):
	weights = collections.defaultdict(int)
	for i in range(numIters):
		print ('Starting iteration ' + str(i) + '...')
		for i in range(len(trainExamples)):
			decimal.getcontext().prec = 100
			x = trainExamples[i][0]
			y = decimal.Decimal(trainExamples[i][1])
			features = featureExtractor(x)
			e = decimal.Decimal(math.e)
			for k2, v2 in features.items():
				decimalWeight = decimal.Decimal(weights[k2])
				V2 = decimal.Decimal(v2)
				firstTerm = decimal.Decimal(1/(1+(e**(-1*decimalWeight*V2*y))))
				secondTerm = decimal.Decimal((-1*(e**(-1*decimalWeight*V2*y))))
				thirdTerm = decimal.Decimal(V2*y)
				lossLogistic = float(firstTerm*secondTerm*thirdTerm)
				weights[k2] = weights[k2] - (eta*lossLogistic)

	print (weights)
	return weights


def mean(numbers):
	return sum(numbers)/float(len(numbers))

def stdev(numbers):
	avg = mean(numbers)
	variance = sum([pow(x-avg, 2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)

def calculateProbability(x, mean, stdev):
	exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
	return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent

# Dictionary with key -- label, value -- array of feature vectors
def separateTrainingExamplesByClass(trainingExamples):
	dataByClass = collections.defaultdict()

	for trainingExample in trainingExamples:
		label = trainingExample[1]
		feature_vector = featureExtractor(trainingExample[0])
		if label in dataByClass:
			array = dataByClass[label]
			array.append(feature_vector)
			dataByClass[label] = array
		else:
			dataByClass[label] = [feature_vector]

	return dataByClass


def summarizeClassData(classData):
	dp = classData[0]

	grouped_features = collections.defaultdict()

	for datapoint in classData:
		for feature in feature_list:
			# if this isnt true, add a 0
			if feature in datapoint:
				number = datapoint[feature]
			else:
				number = 0

			if feature in grouped_features:
				array = grouped_features[feature]
				array.append(number)
				grouped_features[feature] = array
			else:
				grouped_features[feature] = [number]

	# Mean and stdev for each feature
	summarized_feature_vector = collections.defaultdict()
	for feature, feature_values in grouped_features.items():
		feature_mean = mean(feature_values)
		feature_stdev = stdev(feature_values)
		summarized_feature_vector[feature] = [feature_mean, feature_stdev]

	return summarized_feature_vector


# Takes a test example and returns class with higher probability
def bayesPredictor(non_billboard_summarized, billboard_summarized, testExample):
	billboard_probability = 0
	non_billboard_probability = 0
	example_features = featureExtractor(testExample)

	for feature in feature_list:
		if feature in example_features:
			number = example_features[feature]
		else:
			number = 0

		billboard_feature_stats = billboard_summarized[feature]
		non_billboard_feature_stats = non_billboard_summarized[feature]

		if billboard_feature_stats[1] != 0:
			prob = calculateProbability(number, billboard_feature_stats[0], billboard_feature_stats[1])
			if prob > 0:
				billboard_probability += math.log(prob)

		if non_billboard_feature_stats[1] != 0:
			prob = calculateProbability(number, non_billboard_feature_stats[0], non_billboard_feature_stats[1])
			if prob > 0:
				non_billboard_probability += math.log(prob)

	if billboard_probability > non_billboard_probability:
		return 1

	return -1

# Run python billboard.classifier.py -h for options
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
	elif args.c == 'bayes':

		#TODO: Add class probabilities (**)
		separated_data = separateTrainingExamplesByClass(trainingExamples)
		non_billboard_summarized = summarizeClassData(separated_data[-1])
		billboard_summarized = summarizeClassData(separated_data[1])
		testExamples = labelTestExamples(dataset)
		totalTested = len(testExamples)
		correct = 0
		tp = 0
		fp = 0
		fn = 0
		tn = 0

		for testExample in testExamples:
			prediction = bayesPredictor(non_billboard_summarized, billboard_summarized, testExample[0])
			actual = testExample[1]

			if actual == 1 and prediction == 1:
				tp += 1
			if prediction == 1 and actual == -1:
				fp += 1
			if prediction == -1 and actual == 1:
				fn += 1
			if (actual == prediction):
				correct += 1

		print (correct)
		print (totalTested)
		percentageCorrect = float(correct) / float(totalTested)
		print ("Accuracy: " + str(percentageCorrect))
		print ("Precision: " + str(float(tp)/ (float(tp) + float(fp))))
		print ("Recall: " + str(float(tp)/ (float(tp) + float(fn))))
		sys.exit(2)
	elif args.c == 'logistic':
		weights = learnPredictorLogistic(trainingExamples, numIters, eta)
	else:
		weights = learnPredictorRegular(trainingExamples, numIters, eta)

	sortedWeights = sorted(weights.items(), key=lambda x: x[1])
	print(sortedWeights)
	testExamples = labelTestExamples(dataset)
	evaluatePredictor(testExamples, weights, predictor, args.c)

if __name__ == "__main__":
	main(sys.argv[1:])
