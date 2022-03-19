import requests
import ast
import sys
import os

def Create_backup():
	print('Creating backup...')

	SONGS_PATH = os.getenv('LOCALAPPDATA') + '/osu!/Songs'

	if not os.path.exists(SONGS_PATH):
		try:
			FILE = open('songs_path.txt', 'r')
			SONGS_PATH = FILE.read()
		except:
			correct_path = open('songs_path.txt', 'w')
			correct_path.close()
			print('[ERROR]: Path %LOCALAPPDATA%/osu!/Songs does not exist. Put correct path into songs_path.txt and try again.')
			print('Example: C:/Users/username/AppData/local/osu!/Songs .')
			sys.exit()

	MAP_FOLDERS_LIST = os.listdir(str(SONGS_PATH))

	BACKUP = open('backup.txt', 'w')
	BACKUP.write(str(MAP_FOLDERS_LIST))
	BACKUP.close()

	print('Backup created')
	input('Press [ENTER] to exit.')

def Read_backup():
	try:
		MAP_FOLDERS_LIST = open('backup.txt', 'r').read()
	except:
		print('backup.txt file not found.')

	MAP_FOLDERS_LIST = ast.literal_eval(MAP_FOLDERS_LIST)
	MAP_ID = []
	i = 0

	DOWNLOADS_PATH = os.getcwd() + '/backup_downloads'

	if not os.path.exists(DOWNLOADS_PATH):
		print('Creating folder for beatmaps at ' + DOWNLOADS_PATH)
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
			print('[FILE] ' + MAP_FOLDERS_LIST[i] + ' Saved at ' + DOWNLOADS_PATH)
		i += 1
	print()
	print('All beatmap downloaded')
	input('Press [ENTER] to exit.')

print('''
	Choose an option:
	1. Create backup.
	2. Download beatmaps from backup.
	0. EXIT\n
	''')
print('Type number (1-2)\n')

choice = input()
choice = int(choice)

if choice == 0:
	sys.exit()
elif choice == 1:
	choice = Create_backup()
elif choice == 2:
	choice = Read_backup()