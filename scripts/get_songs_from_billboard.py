import billboard
import time
import datetime


def getPrevWeek(date):
	dateArray = date.split('-')
	year = int(dateArray[0])
	month = int(dateArray[1])
	day = int(dateArray[2])
	currentDate = datetime.date(year, month, day)
	lastWeek = currentDate - datetime.timedelta(days=7)
	lastWeek = str(lastWeek)
	return lastWeek

chart = billboard.ChartData('rap-song')
f = open("../song_info/billboard-song-attributes.txt", "w")
alreadyInSongs = set([])
numOfSongsAdded = 0


chart = billboard.ChartData('rap-song')
prevDate = ''
while True:
	if not chart:
		while not chart:
			prevDate = getPrevWeek(prevDate)
			chart = billboard.ChartData('rap-song', prevDate)
	prevDate = chart.previousDate
	if numOfSongsAdded >= 1273:
		break
	for entry in chart.entries:
		titleArtist = entry.title + entry.artist
		if titleArtist in alreadyInSongs:
			continue

		alreadyInSongs.add(titleArtist)
		f.write(str(entry.title) + ':' + str(entry.artist) + ':' + str(entry.peakPos) + ':' + str(chart.date) + '\n')
		numOfSongsAdded += 1
	time.sleep(1)
	chart = billboard.ChartData('rap-song', chart.previousDate)

print(str(numOfSongsAdded))