import json, base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pymenu import Menu

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
    fecha_vencimiento = input("Ingrese fecha vencimiento (YYYY-mm-dd): ")
    etiqueta = input("Ingrese etiqueta: ")
    agregar_tarea(titulo, desc, fecha_vencimiento, etiqueta)
    menu_principal()

def mostrar_tareas_ui():
    if len(tareas) == 0:
        print("No hay tareas.")
    for key, value in tareas.items():
        print(f"[ID {key}]")
        print(
f"""  Título: {value["titulo"]}
  Descripción: {value["descripcion"]}
  Fecha de vencimiento: {value["fecha_vencimiento"]}
  Etiqueta: {value["etiqueta"]}
""")
    input("Presiona enter para continuar.")
    menu_principal()
    

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

# Busca la tarea por criterio
# (ejemplo, criterio: "titulo" y valor "A" retorna la tarea de título "A") 
def get_tarea_id_by(criterio: str, valor: str):
    global tareas
    for id, tarea in tareas.items():
        if tarea[criterio] == valor:
            return id
    return None

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
    ("Salir", salir)
])

def menu_principal():
    menu.show()

cargar_tareas()
menu_principal()