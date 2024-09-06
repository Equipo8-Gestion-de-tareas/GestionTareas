import json, base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Style
from pymenu import Menu
from datetime import datetime

tareas = {}
f = None
usr = ""

def set_user_data(user_pass: str, user_name: str):
    global f, usr
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        iterations=480000,
        salt = bytes(0)
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(user_pass, encoding="UTF-8")))
    f = Fernet(key)
    usr = user_name

def agregar_tarea_ui():
    titulo = input("Ingrese título: ")
    desc = input("Ingrese descripción: ")
    incorrecto = True
    while incorrecto:
        try:
            fecha_vencimiento = input("Ingrese fecha vencimiento (YYYY-mm-dd): ")
            parse_fecha(fecha_vencimiento)
            incorrecto = False
        except ValueError:
            print(Fore.RED + "Formato incorrecto, por favor reintentar." + Style.RESET_ALL)
    etiqueta = input("Ingrese etiqueta: ")
    agregar_tarea(titulo, desc, fecha_vencimiento, etiqueta)
    menu_principal()

def mostrar_tareas_ui():
    if len(tareas) == 0:
        print("No hay tareas.")
    for key, value in tareas.items():
        print(f"\n[ID {key}]")
        print_tarea(value)
    input("Presiona enter para continuar.")
    menu_principal()

def resultado_busqueda_ui(criterio: str):
    busq = input("Ingresar búsqueda: ")
    res = get_tareas_by(criterio, busq)
    if not res:
        print("No hay resultados.")
    else:
        for tarea in res:
            print_tarea(tarea)
    input("Enter para continuar.")
    menu_principal()

def buscar_tarea_ui():
    menu_busqueda = Menu("Elegir criterio de búsqueda")
    menu_busqueda.add_options([
    ("Título", lambda: resultado_busqueda_ui("titulo")),
    ("Descripción", lambda: resultado_busqueda_ui("descripcion")),
    ("Fecha", lambda: resultado_busqueda_ui("fecha_vencimiento")),
    ("Etiqueta", lambda: resultado_busqueda_ui("etiqueta"))
    ])
    menu_busqueda.show()

def parse_fecha(fecha: str) -> datetime:
    return datetime.strptime(fecha, "%Y-%m-%d")

def print_tarea(tarea):
    print(f'  Título: {tarea["titulo"]}')
    print(f'  Descripción: {tarea["descripcion"]}')
    print(f'  Fecha de vencimiento: {tarea["fecha_vencimiento"]}')
    print(f'  Etiqueta: {tarea["etiqueta"]}')
    if(parse_fecha(tarea["fecha_vencimiento"]) < datetime.now()):
        print(Fore.RED + "ATRASADA" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "A tiempo" + Style.RESET_ALL)


def agregar_tarea(titulo: str, descripcion: str, fecha_vencimiento: str, etiqueta: str):
    global tareas
    tarea = {}
    tarea["titulo"] = titulo
    tarea["descripcion"] = descripcion
    tarea["fecha_vencimiento"] = fecha_vencimiento
    tarea["etiqueta"] = etiqueta
    if not tareas:
        tareas[0] = tarea
        return
    ultimo_id = list(tareas.keys())[-1]
    tareas[ultimo_id + 1] = tarea
    guardar_tareas()


def get_tareas_by(criterio: str, valor: str):
    global tareas
    res = []
    for id, tarea in tareas.items():
        if valor in tarea[criterio]:
            res.append(tarea)
    return res

def guardar_tareas():
    global tareas
    json_tareas = json.dumps(tareas)
    if json_tareas == "":
        json_tareas = "{}"
    encryp = f.encrypt(bytes(json_tareas, encoding="utf-8"))
    with open("./db/tareas-"+usr+".enc", "w") as file:
        file.write(encryp.decode("utf-8"))
        

def _int_keys(d):
    try:
        new = {int(k):v for k,v in d.items()}
        return new
    except ValueError:
        return d

def cargar_tareas():
    global tareas
    try:
        with open("./db/tareas-"+usr+".enc", "r") as file:
            encryp = file.read()
    except FileNotFoundError:
        new = open("./db/tareas-"+usr+".enc", "w")
        new.close()
        return
    encryp = bytes(encryp, encoding="utf-8")
    dec = f.decrypt(encryp).decode("utf-8")
    tareas = json.loads(dec, object_hook=_int_keys)

def salir():
    guardar_tareas()
    quit()

set_user_data("woww", "woww")

menu = Menu("Gestión de tareas")
menu.add_options([
    ("Agregar tareas", agregar_tarea_ui),
    ("Mostrar todas las tareas", mostrar_tareas_ui),
    ("Buscar tareas", buscar_tarea_ui),
    ("Salir", salir)
])

def menu_principal():
    menu.show()

cargar_tareas()
guardar_tareas()
menu_principal()