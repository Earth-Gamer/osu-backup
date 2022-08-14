import sys

from loguru import logger
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from . import create_backup
from . import read_backup
from . import Settings

Main_Menu_choices = [
	"Create backup",
	"Download beatmaps from backup",
	"Settings",
	Separator(),
	Choice(value=None, name="Exit"),
]

Settings_Menu_choices =[]

@logger.catch
def Main_Menu():
	action = inquirer.select(
		message = "Choose an option:",
		choices = Main_Menu_choices,
		default = None,
	).execute()

	if action == Main_Menu_choices[0]:
		create_backup.Create_backup()
	elif action == Main_Menu_choices[1]:
		read_backup.Read_Backup()
	elif action == Main_Menu_choices[2]:
		Settings_Menu()

@logger.catch
def Settings_Menu():
	Settings.Menu_Parser()
	Settings_Menu_choices.append(Separator(),)
	Settings_Menu_choices.append(Choice(value=None, name="Exit"),)
	action = inquirer.select(
		message = "Settings:",
		choices = Settings_Menu_choices,
		default = None,
	).execute()

	Settings.Change_Settings(action)