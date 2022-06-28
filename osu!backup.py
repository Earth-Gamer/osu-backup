import configparser
import json
import time
import ast
import sys
import os
import re

import requests
from loguru import logger

@logger.catch
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
				sys.exit()
			else:
				sys.exit()


@logger.catch
class Create_backup:
	def __init__(self):
		Create_backup.Beatmaps_Path_Check(self)
		Create_backup.Write_Backup(self)


	def Beatmaps_Path_Check(self):
		logger.info('Creating backup...')
		Config_Manager.Info_parser(self)

		if self.songs_path == 'default': 
			self.songs_path = os.getenv('LOCALAPPDATA') + '/osu!/Songs'

		if not os.path.exists(self.songs_path):
			logger.error(f'[ERROR]: Path {self.songs_path} does not exist. Type correct path and try again.')
			logger.info('Example: C:/Users/username/AppData/local/osu!/Songs.')

			input_data = input()
			self.songs_path = str(input_data)
			config.set('Settings', 'songs_path', input_data)

			with open('config.ini', 'w') as config_file:
				config.write(config_file)


	def Write_Backup(self):
		MAP_FOLDERS_LIST = os.listdir(str(self.songs_path))
		MAP_id = []
		MAPNAME = []
		beatmaps_dict = {}
		forbidden_chars = '[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]'

		time.sleep(1)
		logger.info('Extracting maps information...')
		for beatmaps in MAP_FOLDERS_LIST:
			result = re.match(forbidden_chars, beatmaps)
			if not result:
				splitter = beatmaps.split(' ', 1)
				MAP_id.append(splitter[0])
				MAPNAME.append(splitter[-1])
		result = json.dumps(dict(zip(MAP_id, MAPNAME)), sort_keys = False, indent=4)

		BACKUP = open('backup.txt', 'w')
		BACKUP.write(str(result))
		BACKUP.close()

		time.sleep(2)
		logger.info('Backup created')
		time.sleep(1)
		input('Press [ENTER] to exit.')


@logger.catch
class Read_Backup:
	global misslist_id
	global misslist_title
	global download_path
	download_path = os.getcwd() + '/backup_downloads'
	misslist_id = []
	misslist_title = []
	backup = {}

	def __init__(self):
		Read_Backup.Backup_Parser(self)
		Read_Backup.Remove_existing_beatmaps(self)
		Read_Backup.Downloader(self)
		logger.info('All beatmaps downloaded')
		logger.info('Press [ENTER] to exit.')
		input()


	def Backup_Parser(self):
		Config_Manager.Info_parser(self)

		global backup
		backup = open(f'{self.backup_path}/backup.txt', 'r').read()
		backup = ast.literal_eval(backup)


	def Downloader(self):
		if not os.path.exists(download_path):
			logger.info('Creating folder for beatmaps at ' + download_path)
			os.makedirs(download_path)

		logger.info('Downloading beatmaps...')
		for self.MapId in self.FilteredBeatmaps:
			Read_Backup.Beatconnect_Parser(self)
		Read_Backup.Missed_Maps()


	def Remove_existing_beatmaps(self):
		self.FilteredBeatmaps = {}
		for Beatmaps in backup:
			downloaded_file_path = f'{download_path}/{Beatmaps} {backup[Beatmaps]}.osz'
			Local_songs_path = f'{self.songs_path}/{Beatmaps} {backup[Beatmaps]}'
			if not os.path.isdir(Local_songs_path):
				if not os.path.isfile(downloaded_file_path): 
					self.FilteredBeatmaps[Beatmaps]=backup[Beatmaps]


	def Beatconnect_Parser(self):
		download_url = 'https://beatconnect.io/b/'
		try:
			self.response = requests.get(download_url + self.MapId)
		except requests.Timeout:
			misslist_id.append(self.MapId)
			misslist_title.append(backup[self.MapId])
			logger.exception('Connection Timeout. Reconnecting 2 minutes.')
			time.sleep(120)

		logger.info(f'[DOWNLOAD] {backup[self.MapId]}')
		global status_code
		status_code = self.response.status_code
		if status_code != requests.codes.ok:
			Read_Backup.Request_Errors(self)
		else:
			Read_Backup.Write_Beatmap(self)
		time.sleep(30)


	def Request_Errors(self):
		if status_code == 404:
			logger.error(f'File <{backup[self.MapId]}> failed to download.')
			misslist_id.append(self.MapId)
			misslist_title.append(backup[self.MapId])

		elif status_code == 502:
			logger.error("somthing went wrong with connection, we will try again after 60 seconds.")
			misslist_id.append(self.MapId)
			misslist_title.append(backup[self.MapId])
			time.sleep(60)


	def Write_Beatmap(self):
		self.ErrorStatus = False
		with open(os.path.join(download_path, f'{self.MapId} {backup[self.MapId]}.osz'), 'wb') as f:
			f.write(self.response.content)
		logger.info("[FILE] dowloaded.")
			

	def Missed_Maps():	
		if misslist_id and misslist_title != None:
			result = json.dumps(dict(zip(misslist_id, misslist_title)), sort_keys = False, indent=4)
			with open('missing_beatmaps.txt', 'w') as f:
				f.write(result)
			logger.warning('Some beatmaps did not download. Try to install them manually on "https://osu.ppy.sh/beatmapsets"')
	

@logger.catch
class Config_Manager:
	def __init__(self):
		Config_Manager.Load_Config_Check()
		Config_Manager.Info_parser(self)


	def Load_Config_Check():
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
			logger.error('config file not found')
			Config_Manager.Create_Config()
	

	def Info_parser(self):
		config = configparser.ConfigParser()
		config.read('config.ini')

		self.songs_path = config.get('Settings', 'songs_path')
		if self.songs_path == 'default':
			self.songs_path = os.getenv('LOCALAPPDATA') + '/osu!/Songs'
		
		self.backup_path = config.get('Settings', 'backup_path')
		if self.backup_path == 'default':
			self.backup_path = os.getcwd()


	def Create_Config():
		# Default config
		template = {
			'songs_path':'default', # default -> %LOCALAPPDATA%/osu!/Songs
			'backup_path':'default', # default -> current directory
		}

		config = configparser.ConfigParser()
		config.add_section('Settings')
		config.set('Settings', 'songs_path', template['songs_path'])
		config.set('Settings', 'backup_path', template['backup_path']) 
		with open('config.ini', 'w') as config_file:
			config.write(config_file)


@logger.catch
def Main():
	logger.add(
	"{time}.log", 
	format="{time:YYYY-MM-DD at HH:mm:ss} | {level}  <{message}>",
	level="TRACE"
	)

	logger.trace('Main menu')
	print('''
		Choose an option:
		1. Create backup.
		2. Download beatmaps from backup.
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
		Read_Backup()

if __name__ == "__main__":
	Config_Manager()
	Main()
