import os, random, operator, sys, re, textblob

def dotProduct(d1, d2):
    """
    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param dict d2: same as d1
    @return float: the dot product between d1 and d2
    """
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def increment(d1, scale, d2):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.
    """
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale


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
	song = firstLine + ' ' + song[song.find('\n') + 1:]
	return song

def labelTrainingExamples(dataset):
	inBillboardDirectory = '../lyrics/'+ dataset + '/billboard-lyrics/training-set'
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

	outOfBillboardDirectory = '../lyrics/' + dataset + '/non-billboard-lyrics/training-set'
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


def labelTestExamples(dataset):
	inBillboardDirectory = '../lyrics/' + dataset + '/billboard-lyrics/validation-set'
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

	outOfBillboardDirectory = '../lyrics/' + dataset + '/non-billboard-lyrics/validation-set'
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



def evaluatePredictor(testExamples, weights, predictor, classifier):
	#testExamples = labelTestExamples()
    totalTested = len(testExamples)
    correct = 0
    tp = 0
    fp = 0
    fn = 0
    tn = 0

    count = 0
    for testExample in testExamples:

        prediction = predictor(testExample[0], weights, classifier)
        actual = testExample[1]
        if actual == 1 and prediction == 1:
            tp += 1
        if prediction == 1 and actual == -1:
            fp += 1
        if prediction == -1 and actual == 1:
            fn += 1
        if (actual == prediction):
            correct += 1


        # print ('Test example ' + str(count))
        # print ('CORRECT') if (actual == prediction) else print ('INCORRECT')
        # print ('Prediction: ' + str(prediction) + ', Actual: ' + str(actual))
        # print ('')


        count += 1

    print (correct)
    print (totalTested)
    percentageCorrect = float(correct) / float(totalTested)
    print ("Accuracy: " + str(percentageCorrect))
    print ("Precision: " + str(float(tp)/ (float(tp) + float(fp))))
    print ("Recall: " + str(float(tp)/ (float(tp) + float(fn))))
