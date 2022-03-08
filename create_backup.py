import os

SONGS_PATH = os.getenv('LOCALAPPDATA') + '/osu!/Songs'
MAP_FOLDERS_LIST = os.listdir(SONGS_PATH)

BACKUP = open('backup.py', 'w')
BACKUP.write('MAP_FOLDERS_LIST = ' + str(MAP_FOLDERS_LIST))
BACKUP.close()