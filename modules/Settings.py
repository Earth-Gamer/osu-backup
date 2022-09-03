import configparser

from loguru import logger

from . import interface


@logger.catch
def Main_Menu_Parser():
	config = configparser.ConfigParser()
	config.read('config.ini')
	for value in config['Settings']:
		interface.config_variables.append(value)

@logger.catch
class ChangeCofigParams:
	def Option_Parser(option):
		config = configparser.ConfigParser()
		config.read('config.ini')

		option_data = config.get('Settings', option)
		return option_data

	def Write_Settings(option, action):
		config = configparser.ConfigParser()
		config.read('config.ini')

		config.set('Settings', option, action)
		with open('config.ini', 'w') as config_file:
			config.write(config_file)

		logger.info("Settings changed")