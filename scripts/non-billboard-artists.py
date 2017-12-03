import requests
import urllib
import re
import os
import time
from bs4 import BeautifulSoup
import http
import random
artists = []
billboardArtists = []
SONGS_PER_ARTIST = 4
song_list = []
numRetrieved = 0


with open('../song_info/billboard-artists.txt') as f:
  lines = f.readlines()
  for artist in lines:
    billboardArtists.append(artist.replace('\n', ''))

numLines = 0
numTossed = 0
with open('../song_info/non-billboard-artists-all.txt') as f:
  lines = f.readlines()
  numLines = len(lines)
  for artist in lines:
    artist = artist.replace('\n', '')
    if '(' in artist:
      artist = artist.split('(')[0]

    if artist in billboardArtists:
      numTossed += 1
      print ('Tossing out billboard artist: ' + str(artist))
    else:
      artists.append(artist)

print ('Total artists in OHHLA database -- ' + str(numLines))
print ('Total billboard artists tossed out --  ' + str(numTossed))
print ('Total remaining -- ' + str(len(artists)))


i = 1
count = 0
urls = []


#script crashed midway a couple times ):
for artist in artists[2942:]:
  print ('')
  print('******ARTIST ' + str(i) + ': ' + artist + ' ******')
  i = i + 1

  artist_url = artist.replace(' ', '-')
  artist_url = artist.replace('.', '')
  artist_suffix = artist_url + '-lyrics'

  artist_url = 'http://www.songlyrics.com/' + artist_suffix

  if artist_url in urls:
    continue
  req = urllib.request.Request(artist_url, headers={'User-Agent' : 'Magic Browser'})
  try:
    page = urllib.request.urlopen(req)
  except urllib.error.HTTPError:
    print('Url not found: ' + artist + ' (' + artist_url + ')')
    continue

  if page.geturl() in urls:
    print('Url already visited: ' + artist_url)
    continue
  else:
    urls.append(page.geturl())
    count += 1

  print ('Found page for ' + str(artist))

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
    maxSongs = SONGS_PER_ARTIST if len(songsByArtist) > SONGS_PER_ARTIST else len(songsByArtist)
    chosen_songs = random.sample(songsByArtist, maxSongs)
    print ('Randomly chose ' + str(len(chosen_songs)) + ' songs: ' + str(chosen_songs))

    # Retrieve lyrics
    for song in chosen_songs:
      print('Looking for song lyrics...' + str(song))
      if song not in song_list:
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
        file_name = '../lyrics/non-billboard-artist-lyrics/'+artist+':'+song+'.txt'
        f = open(file_name, 'w')
        f.write(song + ':' + artist + '\n')
        f.write(lyricText)
        f.close()
        song_list.append(song+':'+artist)
        numRetrieved += 1
  else:
    print('Could not find song list')

  print ('****************')

# f = open('../song_info/non-billboard-artist-attributes.txt', 'w')
# for song in song_list:
#   f.write(song + '\n')
# f.close()

# print('')
# print('Finished. Retrieved ' + str(numRetrieved) + 'songs')

# print ('Number of artists found pages for: ' + str(count))







