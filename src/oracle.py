import util
import os
import collections

def featureExtractor(x):
	words = x.split()
	words = x
	d = collections.defaultdict(int)
	for word in words:
		d[word] = d[word] + 1
	return d   

def learnPredictor(trainExamples, numIters, eta):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    '''
    weights = {}  # feature => weight
    # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)

       

    weights = collections.defaultdict(int)
    #print trainExamples
    for i in xrange(numIters):
    	if trainExamples == None:
    		print "not reached"
    		continue
    	#print trainExamples[0]
        for i in xrange(len(trainExamples)):
        	x = trainExamples[i][0]
        	y = trainExamples[i][1]
        	#print 'reached'
        	features = featureExtractor(x)
        	margin = y*util.dotProduct(weights, features)
        	if margin < 1:
        		for k2, v2 in features.iteritems():
        			lossHinge = -(v2*y)  #w[k2] should always be here 
        			weights[k2] = weights[k2] - (eta*lossHinge)
        #print "train: " + str(evaluatePredictor(trainExamples, predictor))
        #print "test: " + str(evaluatePredictor(testExamples, predictor))
    #return evaluatePredictor(testExamples, predictor)
    

    return dict(weights)


def predictor(x, weights):
    score = 0
    features = featureExtractor(x)
    #for k, v in features.iteritems():
    #    score = score * weights[k]
    score = util.dotProduct(features, weights)
    if score <= 0:
        return 1
    else:
        return -1

def doNeg(songs):
	newSongs = []
	for i in xrange(len(songs)):
		songs[i].append(-1)
		newTuple = tuple(songs[i])
		newSongs.append(newTuple)
		#newSongs.append((songs[i], -1))
	return newSongs

def doPos(songs):
	newSongs = []
	for i in xrange(len(songs)):
		songs[i].append(1)
		newTuple = tuple(songs[i])
		newSongs.append(newTuple)
		#newSongs.append((songs[i], 1))
	return newSongs

def unpack(artist):
	#list of songs. each song is also in a list by itself
	songs = []
	count = 0
	for filename in os.listdir('training-data/'+artist):
		count += 1
		file = open('training-data/'+artist+'/'+filename, "r")
		if file.readline().startswith('We do not have the lyrics for'):
			file.close()
			continue
		file.close()
		song = ''
		with open('training-data/'+artist+'/'+filename, "r") as myfile:
			song=myfile.read()
		song = [song]
		songs.append(song)
	print str(count)
	return songs

def main():
	#one-vs-one multiclass classification
	#make 3 binary classifiers
	emExample = ''
	with open('training-data/eminem/Superman.txt', "r") as myfile:
		emExample = myfile.read()

	snoopExample = ''
	with open('training-data/snoop-dogg/Can-I-Get-A-Flicc-Witchu-Feat-.txt', "r") as myfile:
		snoopExample = myfile.read()

	wayneExample = ''
	with open('training-data/lil-wayne/6-Foot-7-Foot-Single-.txt', "r") as myfile:
		snoopExample = myfile.read()	

	
	songs = [(emExample, 'eminem'), (snoopExample, 'snoop-dogg'), (wayneExample, 'lil-wayne')]
	
	emTrainEx = unpack("eminem")
	wayneTrainEx = unpack("lil-wayne")
	snoopTrainEx = unpack("snoop-dogg")
	# 20 .01
	#lil wayne vs eminem
	emPos = doPos(emTrainEx)
	wayneNeg = doNeg(wayneTrainEx)
	list1 = emPos[:]
	list1.extend(wayneNeg)
	weight1 = learnPredictor(list1, 100, .01)
	#lil wayne vs snoop dogg
	snoopPos = doPos(snoopTrainEx)
	list2 = wayneNeg[:]
	list2.extend(snoopPos)
	weight2 = learnPredictor(list2, 100, .01)
	#eminem vs snoop doog
	emNeg = doNeg(emTrainEx)
	list3 = emNeg[:]
	list3.extend(snoopPos)
	weight3 = learnPredictor(list3, 100, .01)

	#put examples in each
	for song in songs:
		emVote = 0
		wayneVote = 0
		snoopVote = 0
		if predictor(song[0], weight1) == 1:
			emVote += 1
		else:
			wayneVote += 1
		if predictor(song[0], weight2) == 1:
			snoopVote += 1
		else:
			wayneVote += 1
		if predictor(song[0], weight3) == 1:
			snoopVote += 1
		else:
			emVote += 1
		votes = {"eminem":emVote, "lil-wayne":wayneVote, "snoop-dogg":snoopVote}
		winner = max(votes, key=votes.get)
		print winner + str(votes[winner])
		if winner == song[1]:
			print "successfully predicted " + song[1]
		else:
			print "wrong. Predicted " + winner + ". Answer is " + song[1]

	#create a loop to test and evaluate

if __name__ == "__main__": 
	main()

