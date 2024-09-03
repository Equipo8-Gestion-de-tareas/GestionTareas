import json
import bcrypt
from colorama import Fore, Style
from pymenu import Menu

def create_user(user_name, user_pass):
	with open('./db/users.json', 'r') as users_file:
		users = json.load(users_file)
		users.append({'username': user_name, 'password': hash_password(user_pass)})

	with open('./db/users.json', 'w') as users_file:
		json.dump(users, users_file,indent=4)

def get_user(user_name):
	with open('./db/users.json', 'r') as users_file:
		users = json.load(users_file)
		for user in users:
			if user['username'] == user_name:
				return user
	return dict()

def hash_password(password):
	password_bytes = password.encode('utf-8')
	salt = bcrypt.gensalt()
	password_hash = bcrypt.hashpw(password_bytes, salt)
	return password_hash.decode('utf-8')

def check_password(user_name, user_pass):
	user = get_user(user_name)
	password_hash = user['password'].encode('utf-8')
	user_pass_bytes = user_pass.encode('utf-8')
	passwords_compare = bcrypt.checkpw(user_pass_bytes, password_hash)
	return passwords_compare


def login():
	user_name = input('Ingrese su nombre de usuario: ')
	while not get_user(user_name):
		print(Fore.RED + 'El nombre de usuario no existe, intente nuevamente')
		print(Style.RESET_ALL)
		user_name = input('Ingrese su nombre de usuario: ')
	user_pass = input('Ingrese su contraseña: ')
	while not check_password(user_name, user_pass):
		print(Fore.RED + 'Contraseña incorrecta')
		print(Style.RESET_ALL)
		user_name = input('Ingrese su contraseña: ')
	print(Fore.GREEN + 'Sesión iniciada correctamente')
	print(Style.RESET_ALL)

def signin():
	user_name = input('Ingrese un nombre de usuario: ')
	while get_user(user_name):
		print(Fore.RED + 'El nombre de usuario ya existente')
		print(Style.RESET_ALL)
		user_name = input('Ingrese un nombre de usuario: ')
	user_pass = input('Ingrese una contraseña: ')
	create_user(user_name,user_pass)
	print(Fore.GREEN + 'Usuario creado correctamente')
	print(Style.RESET_ALL)

login_menu = Menu('App - Gestión de Tareas')
login_menu.add_options([
	('Iniciar sesión', login),
	('Crear una cuenta', signin)
])

login_menu.show()