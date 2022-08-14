import configparser

from loguru import logger

from . import interface

@logger.catch
def Menu_Parser():
	config = configparser.ConfigParser()
	config.read('config.ini')

	for value in config['Settings']:
		# result = config.get('Settings')
		interface.Settings_Menu_choices.append(value)

@logger.catch
def Change_Settings(action):
	pass
