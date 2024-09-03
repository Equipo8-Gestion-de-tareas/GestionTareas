import json

tareas = {}


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
    with open("tareas.json", "w") as file:
        json.dump(tareas, file)

def _int_keys(d):
    try:
        new = {int(k):v for k,v in d.items()}
        return new
    except ValueError:
        return d

def cargar_tareas():
    global tareas
    with open("tareas.json", "r") as file:
        tareas = json.load(file, object_hook=_int_keys)