"""from rauth.service import OAuth2Service

genius = OAuth2Service(
	name='genius',
	authorize_url='https://api.genius.com/oauth/authorize',
	access_token_url='https://api.genius.com/oauth/token',
	client_id='KnpzsrPKLZO3Axz9pp5WKx_4DyWJcXaBUA09dLiIY3dUYC0HhGEgrh0U4cE31AvQ',
	client_secret='jlxWBXIgmjtE0mahQPklj5Btv4VaTiak-jzwvFmUaePgc1uiqqrIuZ0ChADLKUfCmuiSqEkwX5T7hyoQ0NMuzA',
	base_url='https://api.genius.com')"""

import requests
import urllib
import re
import os
import time
#from urllib.request import urlopen
from bs4 import BeautifulSoup

"""html = urlopen('http://www.google.com/')
print(html)"""

artists = ['lil-wayne', 'eminem', 'snoop-dogg']

#for each artist
	#pause for a half second
	#make folder called artist
	#get their list of songs
	#for each song
		#pause for a half second
		#get lyrics, remove ' from song titles or basically anything that is not a letter or num and replace with a '-' but don't put two in a row and remember the last char has a - at the end so not two their also
		#save lyrics in txt file and put in that artists folder



for artist in artists:
	os.makedirs(artist)
	#time.sleep(.5)
	#get artists song page
	artist_url = 'http://www.songlyrics.com/'+ artist + '-lyrics/'
	areq = urllib.request.Request(artist_url, headers={'User-Agent' : 'Magic Browser'})
	acon = urllib.request.urlopen(areq)

	asoup = BeautifulSoup(acon, 'html.parser')
	songlist = asoup.find('table', class_='tracklist')
	table_body = songlist.find('tbody')
	rows = table_body.find_all('tr')

	#get all songs from page
	song_titles = []
	for row in rows:
		cols = row.find_all('td')
		song_title = cols[1]
		song_title_text = song_title.text.strip()
		song_titles.append(song_title_text)


	for song in song_titles:
		#time.sleep(.5)

		#reformat song titles to be used in url
		song = re.sub('[^0-9a-zA-Z]+', '-', song)
		#removedDupDash = ''
		"""for i in range(len(song)):
			if i < len(song) - 1:
				if song[i+1] == '-' and song[i] == '-':
					continue
				else:
					removedDupDash += song[i]	
			else:
				removedDupDash += song[i]

		if removedDupDash[len(removedDupDash) - 1] == '-':
			removedDupDash = removedDupDash[:-1]
			song = removedDupDash"""

    	#getsong
		url = 'http://www.songlyrics.com/' + artist + '/' + song + '-lyrics/'
		req = urllib.request.Request(url, headers={'User-Agent' : 'Magic Browser'})
		try:
			con = urllib.request.urlopen(req)
		except urllib.error.HTTPError:
			print ('url wrong: ' + url)
		page = con
		soup = BeautifulSoup(page, 'html.parser')
		#get song lyrics from html
		lyrics = soup.find("p", class_="songLyricsV14 iComment-text")
		if lyrics != None:
			lyricText = lyrics.text.strip()
			file_name = artist +'/'+ song + '.txt'
			f = open(file_name, 'w')
			f.write(lyricText)
			f.close()





