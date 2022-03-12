import os
import sys

print('Creating bacup')

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