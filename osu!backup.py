import configparser
import sys
import json

from loguru import logger

from modules import interface
from modules import config_manager as cfg

version = '1.3.1'

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
			"format":f"{logs_time_format} | {logs_level_format} | {logs_message_format}",
			"level":"TRACE"
		},
	]
}
logger.configure(**config)

@logger.catch
def main():
	logger.trace(f'version: {version}')
	cfg.Config_Manager()
	interface.Main_Menu()

if __name__ == "__main__":
	main()