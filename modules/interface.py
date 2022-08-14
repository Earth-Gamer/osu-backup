import os
import sys

from loguru import logger
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import PathValidator

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

download_from_choices = ['chimu', 'beatconnect']

config_variables = []


@logger.catch
def Main_Menu():
	logger.trace("Main_Menu()")
	action = inquirer.select(
		message = "Choose an option:",
		choices = Main_Menu_choices,
		default = None,
	).execute()
	logger.trace(f"action is:{action}")

	if action == Main_Menu_choices[0]:
		create_backup.Create_backup()
	elif action == Main_Menu_choices[1]:
		read_backup.Read_Backup()
	elif action == Main_Menu_choices[2]:
		Settings_Menu()

@logger.catch
def Settings_Menu():
	logger.trace("Settings_Menu()")
	config_variables.clear()
	Settings.Main_Menu_Parser()
	config_variables.append(Separator(),)
	config_variables.append(Choice(value="Return", name="Return"),)
	config_variables.append(Choice(value=None, name="EXIT"))
	logger.trace(config_variables)
	action = inquirer.select(
		message = "Settings:",
		choices = config_variables,
		default = None,
	).execute()
	logger.trace(f"action is:{action}")
	download_from_index = config_variables.index("download_from")

	if action == "Return":
		config_variables.clear()
		Main_Menu()
	elif action == "download_from":
		ChangeUsingChoiceMenu(action)
	elif action == "songs_path" or "backup_path":
		FilePath_Menu(action)

@logger.catch
def ChangeUsingChoiceMenu(action):
	logger.trace("ChangeUsingChoiceMenu(action)")
	option = action
	option_data = Settings.ChangeCofigParams.Option_Parser(option)
	config_variables.append(Separator(),)
	config_variables.append(Choice(value="Return", name="Return"),)
	config_variables.append(Choice(value=None, name="EXIT"))

	action = inquirer.select(
		message = f"Changing: {option}",
		choices = download_from_choices,
		default = None,
	).execute()
	logger.trace(f"action is:{action}")

	if action == "Return":
		Settings_Menu()

	if action == option_data:
		logger.error('You cannot change the value to itself')
		Settings_Menu()
	else:
		Settings.ChangeCofigParams.Write_Settings(option, action)
		Settings_Menu()

@logger.catch
def FilePath_Menu(action):
	logger.trace("FilePath_Menu(action)")
	option = action
	if action == "songs_path":
		action = inquirer.filepath(
			message = "Type correct filepath:",
			validate=PathValidator(is_dir=True, message="Input is not a directory"),
			only_directories=True,
		).execute()
		logger.trace(action)
		if action != '':
			Settings.ChangeCofigParams.Write_Settings(option, action)
		else:
			logger.error("Input is empty!")
			Settings_Menu()
	elif action == "backup_path":
		home_path = "~/" if os.name == "posix" else "C:\\"
		action = inquirer.filepath(
			message = "Type correct filepath:",
			default=home_path,
			validate=PathValidator(is_file=True, message="Input is not a file"),
			only_files=True,
		).execute()
		logger.trace(action)
		if action != '':
			Settings.ChangeCofigParams.Write_Settings(option, action)
		else:
			logger.error("Input is empty!")
			Settings_Menu()