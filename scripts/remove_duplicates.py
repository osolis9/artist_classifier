from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os


def findDuplicatesInSameDirectory(directory, N):


	#lyricSets = ['validation-set', 'test-set', 'training-set']
	songs = []
	count = 0
	#for songSet in lyricSets:
	for filename in os.listdir(directory):
		if filename == '.DS_Store':
			continue
		#if songSet == 'training-set':
		#	count += 1
		with open(directory+'/'+filename, "r") as myfile:
			songLyric = myfile.read()
			songs.append(songLyric)
	vect = TfidfVectorizer(min_df=1)
	tfidf = vect.fit_transform(songs)
	distanceArray = (tfidf * tfidf.T).A
	distanceArray = np.asarray(distanceArray)
	np.fill_diagonal(distanceArray, float('-inf'))
	distanceArray = np.triu(distanceArray)

	likenessArray = np.flip(np.sort(distanceArray, axis=None), 0)
	print(likenessArray[:100])

	indicesInOrderFromMaxValue = np.argsort(-distanceArray, axis=None)
	
	indexofNMax = np.unravel_index(indicesInOrderFromMaxValue[N], distanceArray.shape)
	print(songs[indexofNMax[0]].split('\n', 1)[0])
	print(songs[indexofNMax[1]].split('\n', 1)[0])
	print(likenessArray[N])
	indexOfMax = np.unravel_index(distanceArray.argmax(), distanceArray.shape)
	print(len(songs))

	for i in range(N+1):
		indexOfSongToDelete = np.unravel_index(indicesInOrderFromMaxValue[i], distanceArray.shape)
		print songs[indexOfSongToDelete[0]].split('\n', 1)[0] + ' || ' + songs[indexOfSongToDelete[1]].split('\n', 1)[0]
	"""for i in range(N+1):
		indexOfSongToDelete = np.unravel_index(indicesInOrderFromMaxValue[i], distanceArray.shape)
		song = songs[indexOfSongToDelete[0]]
		firstLine = song.split('\n', 1)[0]
		firstLineSplit = firstLine.split(':')
		title = firstLineSplit[0]
		#if (title[-1] == '-'):
		#	title = title[:-1]
		artist = firstLineSplit[1]
		file_name = artist + ':' + title + '.txt'
		print(file_name)
		try:
			os.remove(directory+file_name)
		except OSError:
			print 'file not here ' + file_name
			continue"""
	"""print(distanceArray.max())
	print(indexOfMax)
	print songs[indexOfMax[0]]
	print songs[indexOfMax[1]]"""

def getLyrics(directory):
	songs = []
	
	for filename in os.listdir(directory):
		if filename == '.DS_Store':
			continue
		with open(directory+filename, "r") as myfile:
			songLyric = myfile.read()
			songs.append(songLyric)
	return songs

def findDuplicatesAcrossDirectories(N):
	#put billboard songs in 1 list
	#put non-billboard songs in another list
	#find tfidfs of both and find distanceArray
	#sort the distance array so i can visualize which are the biggest
	#find where they stop being the same song
	#delete the song from the non-billboard section
	billboardSongs = getLyrics('billboard-lyrics/')
	nonBillboardSongs = getLyrics('non-billboard-lyrics/')
	songs = billboardSongs[:]
	songs.extend(nonBillboardSongs)
	vect = TfidfVectorizer(min_df=1)
	tfidf = vect.fit_transform(songs)
	#tfidf_billboard = vect.fit_transform(billboardSongs)
	#tfidf_non = vect.fit_transform(nonBillboardSongs)
	#print tfidf_billboard.shape
	#print tfidf_non.shape
	distanceArray = (tfidf * tfidf.T).A
	distanceArray = np.asarray(distanceArray)
	np.fill_diagonal(distanceArray, float('-inf'))
	distanceArray = np.triu(distanceArray)
	print(len(billboardSongs))
	print(len(nonBillboardSongs))
	print(distanceArray.shape)

	likenessArray = np.flip(np.sort(distanceArray, axis=None), 0)
	print(likenessArray[:N])

	indicesInOrderFromMaxValue = np.argsort(-distanceArray, axis=None)
	
	indexofNMax = np.unravel_index(indicesInOrderFromMaxValue[N], distanceArray.shape)
	#print(songs[indexofNMax[0]].split('\n', 1)[0])
	#print(songs[indexofNMax[1]].split('\n', 1)[0])
	#print(likenessArray[N])
	count = 0
	for i in range(N+1):
		indexOfSongToDelete = np.unravel_index(indicesInOrderFromMaxValue[i], distanceArray.shape)
		firstSongLine = songs[indexOfSongToDelete[0]].split('\n', 1)[0]
		secondSongLine = songs[indexOfSongToDelete[1]].split('\n', 1)[0]
		if len(secondSongLine.split(":")) != 2 or len(firstSongLine.split(":")) != 4:
			continue
		
		print str(count) + ' ' + str(likenessArray[i]) + ' ' + firstSongLine + ' || ' + secondSongLine
		firstSongLine = songs[indexOfSongToDelete[0]].split('\n', 1)[0]
		secondSongLine = songs[indexOfSongToDelete[1]].split('\n', 1)[0]
		firstSplit = firstSongLine.split(":")
		secondSplit = secondSongLine.split(":")
		count += 1
		"""if len(secondSplit) == 2:
			if len(firstSplit) == 4:
				title = secondSplit[0]
				artist = secondSplit[1]
				file_name = artist + ':' + title + '.txt'
				print(file_name)
				try:
					os.remove('non-billboard-lyrics/'+file_name)
				except OSError:
					print 'file not here ' + file_name
					continue"""




def removeDuplicatesFeat(directory):
	songs = []
	for filename in os.listdir(directory):
		if filename == '.DS_Store':
			continue
		with open(directory+filename, "r") as myfile:
			songLyric = myfile.read()
			songs.append(songLyric)
	count = 0
	for i in range(len(songs)):
		curFirstLine = songs[i].split('\n', 1)[0]
		curLineSplit = curFirstLine.split(':')
		curTitle = curLineSplit[0]
		curArtist = curLineSplit[1]
		for j in range(len(songs)):
			if i == j:
				continue
			secondFirstLine = songs[j].split('\n', 1)[0]
			secondLineSplit = secondFirstLine.split(':')
			secondTitle = secondLineSplit[0]
			secondArtist = secondLineSplit[1]
			if secondTitle == curTitle:
				firstArtistSplit = curArtist.split()
				secondArtistSplit = secondArtist.split()
				if 'feat' in firstArtistSplit or 'Feat' in firstArtistSplit:
					if 'Featuring' in secondArtistSplit or 'featuring' in secondArtistSplit:
						count += 1
						file_name = curArtist + ':' + curTitle+ '.txt'
						print(file_name)
						try:
							os.remove(directory+file_name)
						except OSError:
							print 'file not here ' + file_name
							continue
	print count


def main():
    #findDuplicatesInSameDirectory('billboard-lyrics/', 28) #ONLY RUN ONCE.I already did it
    #findDuplicatesInSameDirectory('non-billboard-lyrics/', 58)
    #removeDuplicatesFeat('billboard-lyrics/')
    #findDuplicatesAcrossDirectories(200)
    billCount = 0
    nonCount = 0
    for filename in os.listdir('billboard-lyrics'):
    	if filename == '.DS_Store':
    		continue
    	billCount += 1
    for filename1 in os.listdir('non-billboard-lyrics'):
    	if filename1 == '.DS_Store':
    		continue
    	nonCount += 1
    print 'bill count ' + str(billCount)
    print 'non count ' + str(nonCount)
 
if __name__ == "__main__":
    main()