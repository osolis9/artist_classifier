import os

artists = ['lil-wayne', 'eminem', 'snoop-dogg']
for artist in artists:
	count = 0
	for filename in os.listdir('training-data/'+artist):
		file = open('training-data/'+artist+'/'+filename, "r")
		if file.readline().startswith('We do not have the lyrics for'):
			continue
		count += 1
		file.close()
	print "Number of songs for " + artist + " is " + str(count)	 