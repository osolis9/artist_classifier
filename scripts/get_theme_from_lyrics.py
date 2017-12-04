import requests
import json
import collections
import os
import re

AUTH_READ_KEY = 'S3zaadNPijs8'
username = 'uClassify'
classifierName = 'Society-Topics'


def listToDict(l):
  dictionary = collections.defaultdict(float)
  for item in l:
    class_name = item['className']
    p = item['p']
    dictionary[class_name] = float(p)
  return dictionary


def classifyRequest(text):
  url = 'https://api.uclassify.com/v1/'+username+'/'+classifierName+'/'+'classify'
  headers = {'Authorization': 'Token ' + AUTH_READ_KEY}
  data = "{\"texts\": [\"" + text + "\"]}"

  r = requests.post(url, headers=headers, data=data.encode('utf-8'))
  response = json.loads(r.text)[0]
  classifications = response['classification']

  return (listToDict(classifications))

#Dictionary where first line is key
songs = collections.defaultdict()

#Directories for all songs
directories = [
  '../lyrics/all-non-billboard-artist/',
  '../lyrics/dataset_1/billboard-lyrics/test-set',
  '../lyrics/dataset_1/billboard-lyrics/training-set',
  '../lyrics/dataset_1/billboard-lyrics/validation-set',
   '../lyrics/dataset_1/non-billboard-lyrics/test-set',
  '../lyrics/dataset_1/non-billboard-lyrics/training-set',
  '../lyrics/dataset_1/non-billboard-lyrics/validation-set',
]
count = 0
songs = collections.defaultdict()

for directory in directories:
  for filename in os.listdir(directory):
    if filename == '.DS_Store':
      continue

    #Dictionary where first line is key

    count +=1
    with open(directory + '/' + filename, 'r') as f:
      lines = f.readlines()
      firstLine = lines[0]
      firstLine = firstLine.split(':')
      key = ':'.join(firstLine[0:2])
      key = key.replace('\n', '')

      text = ' '.join(lines)
      text = text.replace('\n', '')

      text = re.sub('\W+', ' ', text)

      songs[key] = (classifyRequest(text))

    if count % 10 == 0:
      print ('Processed ' + str(count) + ' songs...')


with open('../song_info/song_themes_1.json', 'a') as fp:
  json.dump(songs, fp, sort_keys=True, indent=4)



