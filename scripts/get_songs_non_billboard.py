import requests
import urllib
import re
import os
import time
from bs4 import BeautifulSoup
import http
import random

urls = []
SONGS_PER_ARTIST = 4
song_list = []
billboard_songs = []
numRetrieved = 0

with open('../song_info/billboard-songs.txt') as f:
  billboardSongs = f.readlines()
  for song in billboardSongs:
    billboard_songs.append(song.replace('\n', ''))


with open('../song_info/billboard-artists.txt') as f:
	billboardArtists = f.readlines()

i = 1
for artist in billboardArtists:
  print ('')

  artist = artist.replace("\n", "")
  print('******ARTIST ' + str(i) + ': ' + artist + ' ******')
  i = i + 1

  artist = artist.replace("\n", "")
  artist_suffix = artist.replace(' ', '-') + '-lyrics'
  artist_url = 'http://www.songlyrics.com/' + artist_suffix
  # Some urls redirect, so keep track of what we've seen
  if artist_url in urls:
    continue

  req = urllib.request.Request(artist_url, headers={'User-Agent' : 'Magic Browser'})
  try:
    page = urllib.request.urlopen(req)
  except urllib.error.HTTPError:
    print('Url not found: ' + artist_url)
    continue

  #Find songs on artist page
  print (page.geturl())
  page = page
  page_url = page.geturl()
  if page_url in urls:
    print('Url already visited: ' + artist_url)
    continue
  else:
    urls.append(page_url)

  print('Url success: ' + artist_url)
  soup = BeautifulSoup(page, 'html.parser')
  songs = soup.find_all('tr', itemprop='itemListElement')
  songsByArtist = []
  if songs != None:
    print ('Found ' + str(len(songs)) + ' songs')
    print ('')
    for song_element in songs:
      song_element_text = song_element.get_text()
      song_element_text = song_element_text.replace('\n', ' ')
      #print (song_element_text)
      song = (''.join(i for i in song_element_text if not i.isdigit()))
      song = song.replace('\t', '')
      song = song.replace('\r', '')
      song = song.strip()
      if len(song) != 0:
        songsByArtist.append(song)
      # song = song.lstrip()

    random.seed(i)
    maxSongs = SONGS_PER_ARTIST if len(songs) > SONGS_PER_ARTIST else len(songs)
    chosen_songs = random.sample(songsByArtist, maxSongs)
    print ('Randomly chosen songs: ' + str(chosen_songs))

    # Retrieve lyrics
    for song in chosen_songs:
      print('Looking for song lyrics...' + str(song))
      if song not in song_list and song not in billboard_songs:
        song = re.sub('[^0-9a-zA-Z]+', '-', song)
        song_url = 'http://www.songlyrics.com/' + artist + '/' + song + '-lyrics/'
        req = urllib.request.Request(song_url, headers={'User-Agent' : 'Magic Browser'})
        try:
          page = urllib.request.urlopen(req)
        except urllib.error.HTTPError:
          print('Song not found: ' + song_url)
          continue

        print('Song found: ' + song_url)
        page = page
        soup = BeautifulSoup(page, 'html.parser')
        lyrics = soup.find('p', class_='songLyricsV14 iComment-text')
        if lyrics != None:
          lyricText = lyrics.text.strip()
        if lyricText.startswith('We do not have the lyrics'):
          print('Lyrics not on website')
          continue
        file_name = '../lyrics/non-billboard-lyrics/'+artist+':'+song+'.txt'
        f = open(file_name, 'w')
        f.write(song + ':' + artist + '\n')
        f.write(lyricText)
        f.close()
        song_list.append(song+':'+artist)
        numRetrieved += 1
  else:
    print('Could not find song list')

  print ('****************')


f = open('../song_info/non-billboard-attributes.txt', 'w')
for song in song_list:
  f.write(song + '\n')
f.close()


print('')
print('Finished. Retrieved ' + str(numRetrieved) + 'songs')




