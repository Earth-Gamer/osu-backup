import requests
import backup 	# backup.py
import os

MAP_FOLDERS_LIST = backup.MAP_FOLDERS_LIST
MAPCOUNT = len(MAP_FOLDERS_LIST)
MAP_ID = []
i = 0 

DOWNLOADS_PATH = os.path.join(os.getenv('LOCALAPPDATA'), 'backup_dowloads')

if not os.path.exists(DOWNLOADS_PATH):
	os.makedirs(DOWNLOADS_PATH)

while i <= MAPCOUNT:
	for mapname in MAP_FOLDERS_LIST:
		splitter = mapname.split(' ')
		MAP_ID.append(splitter[0])	
	i += 1 	

i = 0
while i <= MAPCOUNT:
	for id in MAP_ID:
		MapLink = f'https://beatconnect.io/b/{id}'
		r = requests.get(MapLink)
		with open(os.path.join(DOWNLOADS_PATH, f'{MAP_FOLDERS_LIST[i]}.osz'), 'wb') as f:
			f.write(r.content)
	i += 1