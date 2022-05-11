import requests
import ast
import sys
import os
import time

def Backup_File_Check():
	if not os.path.isfile('backup.txt'):
		try:
			backup = open('temp.txt', 'r')
		except FileNotFoundError:
			print('Failed to find the backup file. Place the backup file in the same folder as the program, and close the program, or enter the backup path here.\nTo close the program press [ENTER].')
			input_data = input()
			if input_data == '':
				sys.exit()
			else:
				tempfile = open('temp.txt', 'w')
				tempfile.write(str(input_data))
				tempfile.close()
				print()
				time.sleep(2)
				print('Program will be closed.')
				time.sleep(2)
				sys.exit()

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
	MAP_ID = []
	MAPNAME = []
	beatmaps_dict = {}
	
	print('Extracting maps information...')
	for beatmaps in MAP_FOLDERS_LIST:
		splitter = beatmaps.split(' ', 1)
		MAP_ID.append(splitter[0])
		MAPNAME.append(splitter[-1])

	result = dict(zip(MAP_ID, MAPNAME))

	BACKUP = open('backup.txt', 'w')
	BACKUP.write(str(result))
	BACKUP.close()

	print('Backup created')
	input('Press [ENTER] to exit.')

def Read_backup():
	try:
		backup = open('backup.txt', 'r').read()
	except:
		backup_path = open('temp.txt', 'r').read()
		backup = open(backup_path + '/backup.txt', 'r').read()

	MAP_ID = ast.literal_eval(backup)
	DOWNLOADS_PATH = os.getcwd() + '/backup_downloads'
	counter = 0

	if not os.path.exists(DOWNLOADS_PATH):
		print('Creating folder for beatmaps at ' + DOWNLOADS_PATH)
		os.makedirs(DOWNLOADS_PATH)

	print('Downloading beatmaps...') 
	for id in MAP_ID:
		MapLink = f'https://beatconnect.io/b/{id}'
		r = requests.get(MapLink)
		print('[DOWNLOAD] ' + MAP_ID[counter])
		with open(os.path.join(DOWNLOADS_PATH, f'{MAP_ID[counter]}.osz'), 'wb') as f:
			f.write(r.content)
			f.close()
			print('[FILE] dowloaded.')
		counter += 1
		
	print()
	print('All beatmap downloaded')
	input('Press [ENTER] to exit.')

class Edit_Backup():
	def __init__(self):
		Edit_Backup.Edit_Menu(self)

	def Edit_Menu(self):
		print('''
		Choose an option:
		1. Add new beatmaps to backup.
		2. Delete beatmaps from backup.
		3. Return to Main menu.
		---------------------------------
		0. EXIT\n
		''')
		print('Type number (0-2)\n')

		choice = input()
		choice = int(choice)

		if choice == 0:
			sys.exit()
		elif choice == 1:
			action = Add_New_Beatmaps()
		elif choice == 2:
			action = Delete_Beatmaps()
		elif choice == 3:
			action = Main()

	def Add_Beatmaps(): 
		pass

	def Delete_Beatmaps():
		pass

	# def Search_Beatmaps():
	# 	pass

def Main(): #
	print('''
		Choose an option:
		1. Create backup.
		2. Download beatmaps from backup.
		3. Edit existing backup.
		---------------------------------
		0. EXIT\n
		''')
	print('Type number (0-2)\n')

	choice = input()
	choice = int(choice)

	if choice == 0:
		sys.exit()
	elif choice == 1:
		Create_backup()
	elif choice == 2:
		Backup_File_Check()
		Read_backup()
	elif choice == 3:
		Backup_File_Check()
		Edit_Backup()

if __name__ == "__main__":
	Main()