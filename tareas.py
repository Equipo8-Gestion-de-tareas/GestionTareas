import json
from cryptography.fernet import Fernet

tareas = {}

#cambiar por funcion!
f = Fernet("o4pXx1VoKQGRM-7MQGLfpOYuN-G2RHfal4qHrUPpM74=")

def agregar_tarea(titulo: str, descripcion: str, fecha_vencimiento: str, etiqueta: str):
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
    for id, tarea in tareas.items():
        if tarea[criterio] == valor:
            return id
    return None

def guardar_tareas():
    json_tareas = json.dumps(tareas)
    encryp = f.encrypt(bytes(json_tareas, encoding="utf-8"))
    with open("./db/tareas.enc", "w") as file:
        file.write(encryp.decode("utf-8"))
        

def _int_keys(d):
    try:
        new = {int(k):v for k,v in d.items()}
        return new
    except ValueError:
        return d

def cargar_tareas():
    global tareas
    with open("./db/tareas.enc", "r") as file:
        encryp = file.read()
    encryp = bytes(encryp, encoding="utf-8")
    dec = f.decrypt(encryp).decode("utf-8")
    tareas = json.loads(dec, object_hook=_int_keys)