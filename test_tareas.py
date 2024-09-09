import pytest
from datetime import datetime
import tareas

@pytest.fixture
def auth():
    tareas.init("user", "pass-hash")
    yield
    tareas.tareas = {}
    tareas.guardar_tareas()

@pytest.fixture
def agregar_tarea(auth):
    tareas.agregar_tarea("titulo", "descripcion", datetime.now(), "etiqueta")

def test_tarea_agregada(auth):
    tareas.agregar_tarea("titulo", "descripcion", datetime.now(), "etiqueta")
    assert len(tareas.tareas) == 1

def test_eliminar_tarea(agregar_tarea):
    tareas.eliminar_tarea(tareas.tareas[0])
    with pytest.raises(KeyError) as e:
        existe = tareas.tareas[0]

def test_editar_tarea(agregar_tarea):
    tareas.editar_campo(tareas.tareas[0], "titulo", "valor_nuevo")
    assert tareas.tareas[0]["titulo"] == "valor_nuevo"

def leer_tarea(agregar_tarea):
    assert tareas.tareas[0]["titulo"] == "titulo"
    assert tareas.tareas[0]["descripcion"] == "descripcion"

def guardar_y_cargar_tarea(agregar_tarea):
    tareas.guardar_tareas()
    tareas.cargar_tareas()
    assert tareas.tareas[0]


pytest.main()