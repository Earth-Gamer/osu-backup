import os
import sys
import ast
import time
import json
import configparser

import requests
from loguru import logger

from . import config_manager as cfg
from . import interface

@logger.catch
class Read_Backup:
	def __init__(self):
		self.misslist_id = []
		self.misslist_title = []
		self.backup = {}
		self.download_path = os.getcwd() + '/backup_downloads'
		
		cfg.Config_Manager.Info_parser(self)
		cfg.Config_Manager.SongsPathCheck(self)
		cfg.Config_Manager.BackupFileCheck(self)
		Read_Backup.Backup_Parser(self)
		Read_Backup.Remove_existing_beatmaps(self)
		Read_Backup.Downloader(self)

		logger.success('All beatmaps downloaded')
		logger.info('Press [ENTER] to exit.')
		input()


	def Backup_Parser(self):
		backup = open(self.backup_path, 'r').read()
		self.backup = ast.literal_eval(backup)


	def Remove_existing_beatmaps(self):
		self.FilteredBeatmaps = {}
		for Beatmaps in self.backup:
			downloaded_file_path = f'{self.download_path}/{Beatmaps} {self.backup[Beatmaps]}.osz'
			Local_songs_path = f'{self.songs_path}/{Beatmaps} {self.backup[Beatmaps]}'
			if not os.path.isdir(Local_songs_path):
				if not os.path.isfile(downloaded_file_path): 
					self.FilteredBeatmaps[Beatmaps]=self.backup[Beatmaps]


	def Downloader(self):
		if not os.path.exists(self.download_path):
			logger.info('Creating folder for beatmaps at ' + self.download_path)
			os.makedirs(self.download_path)

		logger.info('Downloading beatmaps...')
		for self.MapId in self.FilteredBeatmaps:
			Read_Backup.Beatmaps_Parser(self)
		Read_Backup.Missed_Maps(self)


	def Beatmaps_Parser(self):
		logger.trace(self.download_from)
		try:
			self.response = requests.get(self.download_url + self.MapId)
		except requests.Timeout:
			self.misslist_id.append(self.MapId)
			self.misslist_title.append(self.FilteredBeatmaps[self.MapId])
			logger.exception('Connection Timeout. Reconnection in 2 minutes.')
			time.sleep(120)

		logger.info(f'[DOWNLOAD] {self.FilteredBeatmaps[self.MapId]}')
		self.status_code = self.response.status_code
		logger.trace(self.status_code)
		if self.status_code != requests.codes.ok:
			Read_Backup.Request_Errors(self)
		else:
			Read_Backup.Write_Beatmap(self)
		time.sleep(30)


	def Request_Errors(self):
		logger.trace(f'status code is: {self.status_code}')
		logger.error(f'File <{self.FilteredBeatmaps[self.MapId]}> failed to download.')
		self.misslist_id.append(self.MapId)
		self.misslist_title.append(self.FilteredBeatmaps[self.MapId])


	def Write_Beatmap(self):
		with open(os.path.join(self.download_path, f'{self.MapId} {self.FilteredBeatmaps[self.MapId]}.osz'), 'wb') as f:
			f.write(self.response.content)
		logger.success("[FILE] dowloaded.")
			

	def Missed_Maps(self):	
		if self.misslist_id and self.misslist_title != None:
			result = json.dumps(dict(zip(self.misslist_id, self.misslist_title)), sort_keys = False, indent=4)
			with open('missing_beatmaps.txt', 'w') as f:
				f.write(result)
			logger.warning('Some beatmaps are not downloaded. Try to install them manually on "https://osu.ppy.sh/beatmapsets"')