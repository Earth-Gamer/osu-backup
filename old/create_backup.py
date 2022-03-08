import os
import sys

# Инициализация списка и количества карт
SONGS_PATH = open('songs_path.txt','r') 		# путь до песен
MAPLIST = '' 									# Список названий карт
MAPCOUNT = len(MAPLIST) 						# подсчет количества песен в списке
MAP_ID = [] 									# Список ID песен
i = 0

# Проверка существования пути
try:
	MAPLIST = os.listdir(SONGS_PATH.read()) 	# запись названий песен в список
except:
	print("""
		[ERROR]: The path could not be found.\nExample: C:/Users/username/AppData/local/osu!/Songs\n
		""")
	sys.exit()

# # Вытаскиваем код карты
# while i <= MAPCOUNT:
# 	for mapname in MAPLIST: 				# Поочередно выбираем карту
# 		splitter = mapname.split(' ') 		# Разделяем название карты по пробелам
# 		MAP_ID.append(splitter[0])  		# добавляем первое значение в список
# 	i += 1 									# Переходим к следующей карте

# Создание бэкапа
backup = open('backup.py', 'w') 			# Создание .txt бэкап файла
backup.write('MAP_ID = '+ str(MAPLIST))		# Записываем список кодов карт
backup.close()								# Закрываем файл