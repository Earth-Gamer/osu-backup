import re
import os
import sys
import time
import json
import configparser

from loguru import logger

from . import config_manager as cfg
from . import interface

@logger.catch
class Create_backup:
	def __init__(self):
		cfg.Config_Manager.Info_parser(self)
		Create_backup.Beatmaps_Path_Check(self)
		Create_backup.Write_Backup(self)

	def Beatmaps_Path_Check(self):

		if not os.path.exists(self.songs_path):
			logger.error(f'[ERROR]: Path {self.songs_path} does not exist. Type correct path and try again.')
			logger.info('Example: C:/Users/username/AppData/local/osu!/Songs.')
			interface.ChangePathMenu.Menu("songs_path")


	def Write_Backup(self):
		logger.info('Creating backup...')
		MAP_FOLDERS_LIST = os.listdir(str(self.songs_path))
		MAP_ID = []
		MAPNAME = []
		filtered_mapname = []
		forbidden_chars = '[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]'

		time.sleep(1)
		logger.info('Extracting maps information...')
		for beatmaps in MAP_FOLDERS_LIST:
			result = re.match(forbidden_chars, beatmaps)
			if not result:
				splitter = beatmaps.split(' ', 1)
				MAP_ID.append(splitter[0])
				MAPNAME.append(splitter[-1])

		for name in MAPNAME:
			if name.find('[no video]') != -1:
				result = name.replace('[no video]', '')
				result = result.strip()
				filtered_mapname.append(result)


		result = json.dumps(dict(zip(MAP_ID, filtered_mapname)), sort_keys = False, indent=4)

		BACKUP = open('backup.txt', 'w')
		BACKUP.write(str(result))
		BACKUP.close()

		time.sleep(2)
		logger.info('Backup created')
		time.sleep(1)
		logger.info('Press [ENTER] to exit.')
		input()