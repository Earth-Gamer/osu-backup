import requests
import backup
import os
import sys

LOCALDATA = os.getenv('LOCALAPPDATA')
DL_BEATMAPS_PATH = os.path.join(LOCALDATA, 'backup_dowloads')
MAP_ID = backup.MAP_ID 

if not os.path.exists(DL_BEATMAPS_PATH):
	os.makedirs(DL_BEATMAPS_PATH)

# Процесс подключения к сайту
for id in MAP_ID: 
	mapLink = f"https://beatconnect.io/b/{id}" 		# Создаем ссылку с необходимой картой
	try:
		dl = requests.get(mapLink)					# Отправляем запрос на созданную ссылку
		# Запись полученных данных в .osz файл
		with open(os.path.join(DL_BEATMAPS_PATH, f"{id}.osz"), "wb") as f:
			f.write(dl.content)
	except:
		print("[ERROR]: Link was not found.")
		sys.exit()
print("[SUCCESS]: Download completed.")