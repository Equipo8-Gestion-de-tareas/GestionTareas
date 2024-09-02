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
    ultimo_id = tareas.keys()[-1]
    tareas[ultimo_id + 1] = tarea

# Busca la tarea por criterio
# (ejemplo, criterio: "titulo" y valor "A" retorna la tarea de título "A") 
def get_tarea_by(criterio: str, valor: str):
    for tarea in tareas.values():
        if tarea[criterio] == valor:
            return tarea
    return None
