import sys

from loguru import logger
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from . import create_backup
from . import read_backup

Main_Menu_choices = [
	"Create backup",
	"Download beatmaps from backup",
	# "Settings",
	"Exit",
]

@logger.catch
def Main_Menu():
	action = inquirer.select(
		message = "Choose an option:",
		choices = Main_Menu_choices,
		default = None,
	).execute()

	if action == Main_Menu_choices[-1]:
		logger.trace('Exit from programm')
		sys.exit()
	elif action == Main_Menu_choices[0]:
		create_backup.Create_backup()
	elif action == Main_Menu_choices[1]:
		read_backup.Read_Backup()
