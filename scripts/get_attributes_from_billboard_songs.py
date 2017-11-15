def getArtists():
  artists = []
  feature_keywords = ['(Featuring', '(Feat.', '[Featuring', '[Feat.', 'Featuring', 'Feat.', 'F/', 'With']

  f = open('../song_info/billboard-song-attributes.txt')

  for line in f:
    song_attributes = line.split(':')
    artist = song_attributes[1]

    #Cut Features from artist name
    for feature_word in feature_keywords:
      if feature_word in artist:
        artist = artist.split(feature_word)[0]
        break

    artists.append(artist.strip(" "))

  return sorted(list(set(artists)))

def getSongs():
  f = open('../song_info/billboard-song-attributes.txt')
  songs = []
  for line in f:
    song_attributes = line.split(':')
    song = song_attributes[0]
    song = song.replace('\n', '')
    songs.append(song.strip(" "))
  return sorted(list(set(songs)))

artists = getArtists()
f = open('../song_info/billboard-artists.txt', 'r+')
for artist in artists:
    f.write(artist+'\n')
f.close()
print ('Count of unique artists: ' + str(len(artists)))

songs = getSongs()
f = open('../song_info/billboard-songs.txt', 'r+')
for song in songs:
    f.write(song+'\n')
f.close()
print ('Count of unique songs: ' + str(len(songs)))

