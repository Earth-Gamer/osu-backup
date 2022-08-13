import os
import configparser

from loguru import logger

beatconnect_url = 'https://beatconnect.io/b/'
chimu_url = 'https://api.chimu.moe/v1/download/'

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