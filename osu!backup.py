import configparser
import time
import ast
import sys
import os
import re

import requests
# from loguru import logger


# delete or not delete ?

# def Backup_File_Check():
# 	if not os.path.isfile('backup.txt'):
# 		try:
# 			backup = open('temp.txt', 'r')
# 		except FileNotFoundError:
# 			print('Failed to find the backup file. Place the backup file in the same folder as the program, and close the program, or enter the backup path here.\nTo close the program press [ENTER].')
# 			input_data = input()
# 			if input_data == '':
# 				sys.exit()
# 			else:
# 				tempfile = open('temp.txt', 'w')
# 				tempfile.write(str(input_data))
# 				tempfile.close()
# 				print()
# 				time.sleep(2)
# 				print('Program will be closed.')
# 				time.sleep(2)
# 				sys.exit()

def Create_backup():
	print('Creating backup...')
	config = configparser.ConfigParser()
	config.read('config.ini')
	SONGS_PATH = config.get('Settings', 'songs_path')

	if SONGS_PATH == 'default': 
		SONGS_PATH = os.getenv('LOCALAPPDATA') + '/osu!/Songs'
	else:
		SONGS_PATH = os.getenv(str(config))

	if not os.path.exists(SONGS_PATH):
		print(f'[ERROR]: Path {SONGS_PATH} does not exist. Type correct path and try again.')
		print('Example: C:/Users/username/AppData/local/osu!/Songs.')

		input_data = input()
		SONGS_PATH = str(input_data)
		config.set('Settings', 'songs_path', input_data)

		with open('config.ini', 'w') as config_file:
			config.write(config_file)

	MAP_FOLDERS_LIST = os.listdir(str(SONGS_PATH))
	MAP_ID = []
	MAPNAME = []
	beatmaps_dict = {}

	forbidden_chars = '[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]'

	print('Extracting maps information...')
	for beatmaps in MAP_FOLDERS_LIST:
		result = re.match(forbidden_chars, beatmaps)
		if result:
			continue
		else:
			splitter = beatmaps.split(' ', 1)
			MAP_ID.append(splitter[0])
			MAPNAME.append(splitter[-1])
	result = dict(zip(MAP_ID, MAPNAME))

	BACKUP = open('backup.txt', 'w')
	BACKUP.write(str(result))
	BACKUP.close()

	time.sleep(2)
	print('Backup created')
	time.sleep(1)
	input('Press [ENTER] to exit.')

def Read_backup():

	# IMPORTANT: recreate with configparser
	# try:
	# 	backup = open('backup.txt', 'r').read()
	# except:
	# 	backup_path = open('temp.txt', 'r').read()
	# 	backup = open(backup_path + '/backup.txt', 'r').read()

	backup = ast.literal_eval(backup)
	DOWNLOADS_PATH = os.getcwd() + '/backup_downloads'

	if not os.path.exists(DOWNLOADS_PATH):
		print('Creating folder for beatmaps at ' + DOWNLOADS_PATH)
		os.makedirs(DOWNLOADS_PATH)

	print('Downloading beatmaps...')
	for id in backup:
		print('[DOWNLOAD] ' + backup[id])
		MapLink = f'https://beatconnect.io/b/{id}'
		r = requests.get(MapLink)
		with open(os.path.join(DOWNLOADS_PATH, f'{backup[id]}.osz'), 'wb') as f:
			f.write(r.content)
			f.close()
			print('[FILE] dowloaded.')

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
			Add_New_Beatmaps()
		elif choice == 2:
			Delete_Beatmaps()
		elif choice == 3:
			Main()

	def Add_Beatmaps():
		pass

	def Delete_Beatmaps():
		pass

	def Search_Beatmaps():
		pass
	
class Config_Manager():
	def Load_Config():
		config = configparser.ConfigParser()
		try:
			if not os.path.isfile('config.ini'):
				Config_Manager.Create_Config()
			if configparser.MissingSectionHeaderError: #Delete and recreate config file
				os.remove('config.ini')
				Config_Manager.Create_Config()
		except FileNotFoundError:
			print('config file not found')
			Config_Manager.Create_Config()
			
			
	def Create_Config():
		# Default config
		config = configparser.ConfigParser()
		config.add_section('Settings')
		config.set('Settings', 'songs_path', 'default')
		config.set('Settings', 'backup_path', 'default') #default -> current directory
		
		with open('config.ini', 'w') as config_file:
			config.write(config_file)

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
		# Backup_File_Check()
		Read_backup()
	elif choice == 3:
		# Backup_File_Check()
		Edit_Backup()

if __name__ == "__main__":
	Config_Manager.Load_Config()
	Main()
