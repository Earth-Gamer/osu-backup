import os
import sys
import tkinter as tk
from tkinter import filedialog

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
	logger.trace(f"action is: {action}")

	if action == Main_Menu_choices[0]:
		create_backup.Create_backup()
	elif action == Main_Menu_choices[1]:
		read_backup.Read_Backup()
	elif action == Main_Menu_choices[2]:
		Settings_Menu()

@logger.catch
def Settings_Menu():
	logger.trace("Settings_Menu")
	config_variables.clear()
	Settings.Main_Menu_Parser()
	config_variables.append(Separator(),)
	config_variables.append(Choice(value="Return", name="Return"),)
	config_variables.append(Choice(value=None, name="Exit"))
	logger.trace(config_variables)
	action = inquirer.select(
		message = "Settings:",
		choices = config_variables,
		default = None,
	).execute()
	logger.trace(f"action is: {action}")
	download_from_index = config_variables.index("download_from")

	if action == None:
		sys.exit()
	elif action == "Return":
		config_variables.clear()
		Main_Menu()
	elif action == "download_from":
		ChangeUsingChoiceMenu(action)
	elif action == "songs_path" or "backup_path":
		ChangePathMenu.Menu(action)

@logger.catch
def ChangeUsingChoiceMenu(action):
	logger.trace("ChangeUsingChoiceMenu")
	option = action
	option_data = Settings.ChangeCofigParams.Option_Parser(option)
	config_variables.append(Separator(),)
	config_variables.append(Choice(value="Return", name="Return"),)
	config_variables.append(Choice(value=None, name="Exit"))

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
class ChangePathMenu:
	def Menu(action):
		logger.trace('ChangePathMenu')
		option = action
		action = inquirer.select(
			message='Choose an option:',
			choices= [
				'Browse',
				'Type manually',
				Separator(),
				Choice(value='Return', name='Return'),
			],
			instruction = 'ctrl + z'
		).execute()
		logger.trace(f'action is: {action}')

		if action == 'Return':
			Settings_Menu()
		elif action == 'Browse':
			ChangePathMenu.FileDialogChoice(action)
		elif action == 'Type manually':
			if option == 'songs_path':
				ChangePathMenu.DirPath_Menu(option)
			elif option == 'backup_path':
				ChangePathMenu.FilePath_Menu(option)

		
	def FileDialogChoice(action):
		logger.trace("FileDialogChoice")
		option = action
		action = ChangePathMenu.FileDialog()
		if action == '':
			logger.error("Input is empty!")
			ChangePathMenu.Menu(option)
		else:
			try:
				os.getenv(action)
			except:
				logger.error("Invalid file path.")
				ChangePathMenu.Menu(option)	
			Settings.ChangeCofigParams.Write_Settings(option, action)
		Main_Menu()

	def FileDialog():
		root = tk.Tk()
		root.withdraw()
		file_path = filedialog.askopenfilename()
		return file_path

	def FilePath_Menu(option):
		logger.trace("FilePath_Menu")
		home_path = "~/" if os.name == "posix" else "C:\\"
		action = inquirer.filepath(
			default=home_path,
			message='Type correct file path:',
			validate=PathValidator(is_file=True, message="Input is not a file"),
			only_files=True,
		).execute()
		logger.trace(f'action is: {action}')
		if action != home_path:
				Settings.ChangeCofigParams.Write_Settings(option, action)
		else:
			logger.error("Input is empty!")
			Settings_Menu()
		Main_Menu()




	def DirPath_Menu(option):
			logger.trace("DirPath_Menu")
			action = inquirer.filepath(
				message = "Type correct directory path:",
				validate=PathValidator(is_dir=True, message="Input is not a directory"),
				only_directories=True,
			).execute()
			logger.trace(action)
			if action != '':
				Settings.ChangeCofigParams.Write_Settings(option, action)
			else:
				logger.error("Input is empty!")
				Settings_Menu()
			Main_Menu()