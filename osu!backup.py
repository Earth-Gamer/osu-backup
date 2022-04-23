import requests
import ast
import sys
import os
import time

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
	
	print('Extracting maps information...')
	for mapname in MAP_FOLDERS_LIST:
		splitter = mapname.split(' ')
		MAP_ID.append(splitter[0])

	BACKUP = open('backup.txt', 'w')
	BACKUP.write(str(MAP_ID))
	BACKUP.close()

	print('Backup created')
	input('Press [ENTER] to exit.')

def Read_backup():
	try:
		MAP_FOLDERS_LIST = open('backup.txt', 'r').read()
	except:
		print('backup.txt file not found.')

	MAP_FOLDERS_LIST = ast.literal_eval(MAP_FOLDERS_LIST)
	i = 0

	DOWNLOADS_PATH = os.getcwd() + '/backup_downloads'

	if not os.path.exists(DOWNLOADS_PATH):
		print('Creating folder for beatmaps at ' + DOWNLOADS_PATH)
		os.makedirs(DOWNLOADS_PATH)

	print('Downloading beatmaps...')
	for id in MAP_ID:
		MapLink = f'https://beatconnect.io/b/{id}'
		r = requests.get(MapLink)
		print('[DOWNLOAD] ' + MAP_FOLDERS_LIST[i])
		with open(os.path.join(DOWNLOADS_PATH, f'{MAP_FOLDERS_LIST[i]}.osz'), 'wb') as f:
			f.write(r.content)
			f.close()
			print('[FILE] ' + MAP_FOLDERS_LIST[i] + ' dowloaded.')
		i += 1
		
	print()
	print('All beatmap downloaded')
	input('Press [ENTER] to exit.')

class Edit_Backup():
	def __init__(self):
		Edit_Backup.Backup_File_Check(self)
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

	def Backup_File_Check(self): # прверяет есть ли бэкап файл в той же директории что и программа
		if not os.path.isfile('backup.txt'):
			try:
				backup = open('temp.txt', 'r')
			except:
				print('Failed to find the backup file. Place the backup file in the same folder as the program, and close it, or enter the backup path here.\nTo close the program press [ENTER].')
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
		else:
			backup = open('backup.txt', 'r')

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
		action = Create_backup()
	elif choice == 2:
		action = Read_backup()
	elif choice == 3:
		action = Edit_Backup()

if __name__ == "__main__":
	Main()