import json
import os
from colorama import Fore, Style

print(Fore.BLUE + 'Inicializando archivos de la aplicación...' + Style.RESET_ALL)

directory = './db'
if not os.path.exists(directory):
	os.makedirs(directory)

with open('./db/users.json', 'w') as users_file:
	json.dump([], users_file, indent=4)

print(Fore.GREEN + 'Archivos inicializados' + Style.RESET_ALL)