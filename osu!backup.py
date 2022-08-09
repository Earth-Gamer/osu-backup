import configparser
import json
import time
import ast
import sys
import os
import re

import requests
from loguru import logger

logs_time_format = "{time:YYYY-MM-DD at HH:mm:ss}"
logs_level_format = "<level>{level}</level>"
logs_message_format = "<level>{message}</level>"
logs_file_path = './logs/'

config = {
	"handlers": [
		{
			"sink": sys.stderr,
			"format": f"<{logs_level_format}> - <{logs_message_format}>"
		},
		{
			"sink": logs_file_path + "{time}.log",
			"level":"TRACE"
		},
	]
}
logger.configure(**config)


beatconnect_url = 'https://beatconnect.io/b/'
chimu_url = 'https://api.chimu.moe/v1/download/'


@logger.catch
class Create_backup:
	def __init__(self):
		Config_Manager.Info_parser(self)
		Create_backup.Beatmaps_Path_Check(self)
		Create_backup.Write_Backup(self)


	def Beatmaps_Path_Check(self):
		logger.info('Creating backup...')

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
		MAP_ID = []
		MAPNAME = []
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


@logger.catch
class Read_Backup:
	def __init__(self):
		self.misslist_id = []
		self.misslist_title = []
		self.backup = {}
		self.download_path = os.getcwd() + '/backup_downloads'
		
		Config_Manager.Info_parser(self)
		
		Read_Backup.Backup_File_Check()
		Read_Backup.Backup_Parser(self)
		Read_Backup.Remove_existing_beatmaps(self)
		Read_Backup.Downloader(self)

		logger.success('All beatmaps downloaded')
		logger.info('Press [ENTER] to exit.')
		input()


	def Backup_File_Check():
		config = configparser.ConfigParser()
		config.read('config.ini')
		if not os.path.isfile('backup.txt'): # current directory
			backup_path = config.get('Settings', 'backup_path')
			if not os.path.isfile(f'{backup_path}/backup.txt'): # directory from config.ini
				logger.error('Failed to find the backup file. Place the backup file in the same folder as the program, and close the program, or enter the backup path here.\nTo close the program press [ENTER].')
				input_data = input()
				if not input_data == '': # input_data == nothing (user press ENTER without anything)
					backup_path = str(input_data)
					config.set('Settings', 'backup_path', input_data)
	
					with open('config.ini', 'w') as config_file:
						config.write(config_file)
					sys.exit()
				else:
					sys.exit()


	def Backup_Parser(self):
		backup = open(f'{self.backup_path}/backup.txt', 'r').read()
		self.backup = ast.literal_eval(backup)


	def Downloader(self):
		if not os.path.exists(self.download_path):
			logger.info('Creating folder for beatmaps at ' + self.download_path)
			os.makedirs(self.download_path)

		logger.info('Downloading beatmaps...')
		for self.MapId in self.FilteredBeatmaps:
			Read_Backup.Beatmaps_Parser(self)
		Read_Backup.Missed_Maps(self)


	def Remove_existing_beatmaps(self):
		self.FilteredBeatmaps = {}
		for Beatmaps in self.backup:
			downloaded_file_path = f'{self.download_path}/{Beatmaps} {self.backup[Beatmaps]}.osz'
			Local_songs_path = f'{self.songs_path}/{Beatmaps} {self.backup[Beatmaps]}'
			if not os.path.isdir(Local_songs_path):
				if not os.path.isfile(downloaded_file_path): 
					self.FilteredBeatmaps[Beatmaps]=self.backup[Beatmaps]


	def Beatmaps_Parser(self):
		try:
			self.response = requests.get(self.download_url + self.MapId)
		except requests.Timeout:
			self.misslist_id.append(self.MapId)
			self.misslist_title.append(self.backup[self.MapId])
			logger.exception('Connection Timeout. Reconnection in 2 minutes.')
			time.sleep(120)

		logger.info(f'[DOWNLOAD] {self.backup[self.MapId]}')
		self.status_code = self.response.self.status_code
		if self.status_code != requests.codes.ok:
			Read_backup.Request_Errors(self)
		else:
			Read_Backup.Write_Beatmap(self)
		time.sleep(30)


	def Request_Errors(self):
		if self.status_code == 404:
			logger.error(f'File <{self.backup[self.MapId]}> failed to download.')
			self.misslist_id.append(self.MapId)
			self.misslist_title.append(self.backup[self.MapId])

		elif self.status_code == 502:
			logger.error("somthing went wrong with connection, we will try again after 60 seconds.")
			self.misslist_id.append(self.MapId)
			self.misslist_title.append(self.backup[self.MapId])
			time.sleep(60)


	def Write_Beatmap(self):
		with open(os.path.join(self.download_path, f'{self.MapId} {self.backup[self.MapId]}.osz'), 'wb') as f:
			f.write(self.response.content)
		logger.success("[FILE] dowloaded.")
			

	def Missed_Maps(self):	
		if self.misslist_id and self.misslist_title != None:
			result = json.dumps(dict(zip(self.misslist_id, self.misslist_title)), sort_keys = False, indent=4)
			with open('missing_beatmaps.txt', 'w') as f:
				f.write(result)
			logger.warning('Some beatmaps are not downloaded. Try to install them manually on "https://osu.ppy.sh/beatmapsets"')
	

@logger.catch
class Config_Manager:
	def __init__(self):
		Config_Manager.Load_Config_Check()

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

	
	def Create_Config():
		default_params = {
			'songs_path':'default', # default -> %LOCALAPPDATA%/osu!/Songs
			'backup_path':'default', # default -> current directory
			'download_from':'chimu' #Options ["beatconnect" -> Beatconnect.io] ["chimu" -> Chimu.moe]
		}

		config = configparser.ConfigParser(allow_no_value=True)
		config.add_section('Settings')
		config.set('Settings', 'songs_path', default_params['songs_path'])
		config.set('Settings', 'backup_path', default_params['backup_path'])
		config.set('Settings', '#Options ["beatconnect" -> Beatconnect.io] ["chimu" -> Chimu.moe]')
		config.set('Settings', 'download_from', default_params['download_from']) 
		with open('config.ini', 'w') as config_file:
			config.write(config_file)


	def Info_parser(self):
		config = configparser.ConfigParser()
		config.read('config.ini')

		self.songs_path = config.get('Settings', 'songs_path')
		if self.songs_path == 'default':
			self.songs_path = os.getenv('LOCALAPPDATA') + '/osu!/Songs'
		
		self.backup_path = config.get('Settings', 'backup_path')
		if self.backup_path == 'default':
			self.backup_path = os.getcwd()

		self.download_from = config.get('Settings', 'download_from')
		if self.download_from == 'beatconnect':
			self.download_url = beatconnect_url
		elif self.download_from == 'chimu':
			self.download_url = chimu_url


@logger.catch
def Main():
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
		logger.trace('Exit from programm')
		sys.exit()
	elif choice == 1:
		Create_backup()
	elif choice == 2:
		Read_Backup()


if __name__ == "__main__":
	Config_Manager()
	Main()