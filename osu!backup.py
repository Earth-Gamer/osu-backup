import configparser
import json
import time
import ast
import sys
import os
import re

import requests
from loguru import logger

logger.add(
	"{time}.log", 
	format="{time:YYYY-MM-DD at HH:mm:ss}  [{level}]  <{message}>",
	level="TRACE"
	) 

def Backup_File_Check():
	config = configparser.ConfigParser()
	config.read('config.ini')
	if not os.path.isfile('backup.txt'): # current directory
		backup_path = config.get('Settings', 'backup_path')
		print(backup_path)
		if not os.path.isfile(f'{backup_path}/backup.txt'): # directory from config.ini
			print('Failed to find the backup file. Place the backup file in the same folder as the program, and close the program, or enter the backup path here.\nTo close the program press [ENTER].')
			input_data = input()
			if not input_data == '': # input_data == nothing (user press ENTER without anything)
				backup_path = str(input_data)
				config.set('Settings', 'backup_path', input_data)

				with open('config.ini', 'w') as config_file:
					config.write(config_file)


def Create_backup():
	logger.info('Creating backup...')
	config = configparser.ConfigParser()
	config.read('config.ini')
	SONGS_PATH = config.get('Settings', 'songs_path')

	if SONGS_PATH == 'default': 
		SONGS_PATH = os.getenv('LOCALAPPDATA') + '/osu!/Songs'
	else:
		SONGS_PATH = os.getenv(str(config))

	if not os.path.exists(SONGS_PATH):
		logger.error(f'[ERROR]: Path {SONGS_PATH} does not exist. Type correct path and try again.')
		logger.info('Example: C:/Users/username/AppData/local/osu!/Songs.')

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

	time.sleep(1)
	logger.info('Extracting maps information...')
	for beatmaps in MAP_FOLDERS_LIST:
		result = re.match(forbidden_chars, beatmaps)
		if not result:
			splitter = beatmaps.split(' ', 1)
			MAP_ID.append(splitter[0])
			MAPNAME.append(splitter[-1])
	result = json.dumps(dict(zip(MAP_ID, MAPNAME)), sort_keys = False, indent=4)

	BACKUP = open('backup.txt', 'w')
	BACKUP.write(str(result))
	BACKUP.close()

	time.sleep(2)
	logger.info('Backup created')
	time.sleep(1)
	input('Press [ENTER] to exit.')

def Read_backup():
	config = configparser.ConfigParser()
	config.read('config.ini')
	backup_path = config.get('Settings', 'backup_path')

	if backup_path == 'default':
		backup_path = os.getcwd()
	# else: backup_path = string from config file

	backup = open(f'{backup_path}/backup.txt', 'r').read()
	backup = ast.literal_eval(backup)
	DOWNLOADS_PATH = os.getcwd() + '/backup_downloads'

	if not os.path.exists(DOWNLOADS_PATH):
		logger.info('Creating folder for beatmaps at ' + DOWNLOADS_PATH)
		os.makedirs(DOWNLOADS_PATH)

	logger.info('Downloading beatmaps...')
	for id in backup:
		logger.info('[DOWNLOAD] ' + backup[id])
		MapLink = f'https://beatconnect.io/b/{id}'
		try:
			r = requests.get(MapLink)
		except:
			logger.error("Something went wrong when the program tried to connect to the server. Please try again after closing the program.")
			sys.exit(2)
		with open(os.path.join(DOWNLOADS_PATH, f'{backup[id]}.osz'), 'wb') as f:
			f.write(r.content)
			f.close()
			logger.info('[FILE] dowloaded.')

	logger.info('All beatmap downloaded')
	input('Press [ENTER] to exit.')

class Edit_Backup():
	def __init__(self):
		Edit_Backup.Edit_Menu(self)

	def Edit_Menu(self):
		logger.trace('Edit menu')
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
			try:
				config.read('config.ini')
				config.get('Settings', 'songs_path')
			except:
				os.remove('config.ini')
				Config_Manager.Create_Config()
		except FileNotFoundError:
			print('config file not found')
			Config_Manager.Create_Config()
			
	def Create_Config():
		# Default config
		config = configparser.ConfigParser()
		config.add_section('Settings')
		config.set('Settings', 'songs_path', 'default') # %LOCALAPPDATA%/osu!/Songs
		config.set('Settings', 'backup_path', 'default') #default -> current directory
		
		with open('config.ini', 'w') as config_file:
			config.write(config_file)

def Main():
	logger.trace('Main menu')
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
	Config_Manager.Load_Config()
	Main()
