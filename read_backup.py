import requests
import ast
import os

MAP_FOLDERS_LIST = open('backup.txt', 'r').read()
MAP_FOLDERS_LIST = ast.literal_eval(MAP_FOLDERS_LIST)
MAP_ID = []
i = 0

DOWNLOADS_PATH = os.path.join(os.getenv('LOCALAPPDATA'), 'backup_dowloads')

if not os.path.exists(DOWNLOADS_PATH):
	print('Creating folder for beatmaps at' + DOWNLOADS_PATH)
	os.makedirs(DOWNLOADS_PATH)

print('Extracting maps information...')
for mapname in MAP_FOLDERS_LIST:
	splitter = mapname.split(' ')
	MAP_ID.append(splitter[0])	

MAP_ID_COUNT = len(MAP_ID)

print('Downloading beatmaps...')
for id in MAP_ID:
	MapLink = f'https://beatconnect.io/b/{id}'
	r = requests.get(MapLink)
	print('[DOWNLOAD] ' + MAP_FOLDERS_LIST[i])
	with open(os.path.join(DOWNLOADS_PATH, f'{MAP_FOLDERS_LIST[i]}.osz'), 'wb') as f:
		f.write(r.content)
		f.close()
		print('[FILE]' + MAP_FOLDERS_LIST[i] + ' Saved at ' + DOWNLOADS_PATH)
	i += 1

print('All beatmap downloaded')
input('Press [ENTER] to exit.')