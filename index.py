import logging
import json
import bcrypt
import tareas
from colorama import Fore, Style
from uuid import uuid4
from pymenu import Menu, select_menu

logging.basicConfig(level=logging.INFO, filename="logs.txt", format="%(asctime)s [%(levelname)s] - %(message)s")
log = logging.getLogger(__name__)

def get_user_by_name(user_name: str) -> dict:
	with open('./db/users.json', 'r') as users_file:
		users = json.load(users_file)
		for user in users:
			if user['username'] == user_name:
				return user
	return dict()

"""
Login functions
"""
def check_password(user: dict, user_pass: str) -> bool:
	password_hash = user['password'].encode('utf-8')
	user_pass_bytes = user_pass.encode('utf-8')
	passwords_compare = bcrypt.checkpw(user_pass_bytes, password_hash)
	return passwords_compare

def login(user_name: str, user_pass: str) -> int | dict:
	# check if user exists
	user = get_user_by_name(user_name)
	if not user:
		logging.warning('Usuario intenta entrar con un nombre de usuario no registrado')
		return -1
	# check if password is correct
	if not check_password(user, user_pass):
		logging.warning('Usuario intenta entrar con una contraseña incorrecta')
		return -2
	# login success
	return user

def login_ui():
	print(Fore.BLUE + 'Iniciar sesión\n' + Style.RESET_ALL)
	user = 0

	while type(user) == int:
		user_name = input('Ingrese su nombre de usuario: ')
		user_pass = input('Ingrese su contraseña: ')
		user = login(user_name, user_pass)

		if user == -1: # user not exists
			print(Fore.RED + 'El nombre de usuario no existe, intente nuevamente' + Style.RESET_ALL)
		elif user == -2: # password wrong
			print(Fore.RED + 'Contraseña incorrecta, intente nuevamente' + Style.RESET_ALL)

	log.info('Usuario autenticado')
	print(Fore.GREEN + 'Sesión iniciada correctamente.' + Style.RESET_ALL)
	input("Presione enter.")
	tareas.init_ui(user_name, user_pass)

"""
Signin functions
"""
def hash_password(password: str) -> str:
	password_bytes = password.encode('utf-8')
	salt = bcrypt.gensalt()
	password_hash = bcrypt.hashpw(password_bytes, salt)
	return password_hash.decode('utf-8')

def create_user(user_name: str, user_pass: str) -> dict:
	with open('./db/users.json', 'r') as users_file:
		users = json.load(users_file)
		user = {
			'id': str(uuid4()),
			'username': user_name, 
			'password': hash_password(user_pass)
		}
		users.append(user)

	with open('./db/users.json', 'w') as users_file:
		json.dump(users, users_file,indent=4)
	
	log.info('Se ha creado un nuevo usuario en la base de datos')
	return user

def signin(user_name: str, user_pass: str) -> int | dict:
	# check if user exists
	user = get_user_by_name(user_name)
	if not user:
		user = create_user(user_name,user_pass)
		logging.warning('Usuario intenta crear una cuenta con un nombre de usuario ya existente')
		return user
	return -1

def signin_ui():
	print(Fore.BLUE + 'Crear cuenta\n' + Style.RESET_ALL)
	user_name = input('Ingrese un nombre de usuario: ')
	user_pass = input('Ingrese una contraseña: ')
	user = signin(user_name, user_pass)
	while type(user) == int:
		if user == -1: # user exists
			print(Fore.RED + 'El nombre de usuario ya existente, intente nuevamente' + Style.RESET_ALL)
			user_name = input('Ingrese un nombre de usuario: ')
			user_pass = input('Ingrese una contraseña: ')
			user = signin(user_name, user_pass)
	selected_option = select_menu.create_select_menu(['Si', 'No'], 'Su cuenta ha sido creada exitosamente.\n¿Desea iniciar sesión?')
	if selected_option == 'Si':
		login_ui()
	else:
		log.info('Aplicación cerrada')
		exit(1)

def main():
	auth_menu = Menu('App - Gestión de Tareas')
	auth_menu.add_options([
		('Iniciar sesión', login_ui),
		('Crear una cuenta', signin_ui)
	])

	log.info('Aplicación iniciada')
	auth_menu.show()

main()