import requests
import urllib
import re
import os
import time
#from urllib.request import urlopen
from bs4 import BeautifulSoup


#load all the lines into a list
with open('billboard-songs.txt') as f:
	billboardSongs = f.readlines()


artistList = set([])
for song in billboardSongs:
	song = song.split(':')
	artist = song[1]
	featuringArtistIndex = artist.find('Featuring')
	if featuringArtistIndex != -1:
		artist = artist[:featuringArtistIndex-1]
	artistList.add(artist)
print(artistList)

"""numRetrieved = 0
i = 0
for line in billboardSongs:
	print(i)
	i = i+1
	lineList = line.split(":")
	title = lineList[0]
	artist = lineList[1]
	artist = artist.replace('Featuring', 'feat')
	peakRank = lineList[2]
	date = lineList[3]

	#replace anything that is not a letter or num with '-' so that it can be found with a url
	title = re.sub('[^0-9a-zA-Z]+', '-', title)
	song_url = 'http://www.songlyrics.com/' + artist.replace(' ', '-') + '/' + title + '-lyrics/'

	req = urllib.request.Request(song_url, headers={'User-Agent' : 'Magic Browser'})
	try:
		page = urllib.request.urlopen(req)
	except urllib.error.HTTPError:
		print ('url wrong: ' + song_url)
		continue

	page = page
	soup = BeautifulSoup(page, 'html.parser')
	#get song lyrics from html
	lyrics = soup.find("p", class_="songLyricsV14 iComment-text")
	if lyrics != None:
		lyricText = lyrics.text.strip()
		if lyricText.startswith('We do not have the lyrics'):
			print("Lyrics not on website")
			continue
		file_name = 'billboard-lyrics/'+ artist + ':' + title + '.txt'
		f = open(file_name, 'w')
		f.write(title + ':' + artist + ':' + peakRank + ':' + date + '\n')
		f.write(lyricText)
		f.close()
		numRetrieved += 1
print(str(numRetrieved))"""







