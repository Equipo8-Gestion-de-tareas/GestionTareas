import pytest
from datetime import datetime
from cryptography.fernet import InvalidToken
import tareas, os

@pytest.fixture
def auth(autouse=True):
    try:
        os.remove("db/tareas-user.enc")
    except FileNotFoundError:
        pass
    tareas.init("user", "pass-hash")
    yield
    tareas.tareas = {}
    os.remove("db/tareas-user.enc")

@pytest.fixture
def agregar_tarea(auth):
    tareas.agregar_tarea("titulo", "descripcion", datetime.now(), "etiqueta")

def test_tarea_agregada(auth):
    tareas.agregar_tarea("titulo", "descripcion", datetime.now(), "etiqueta")
    assert len(tareas.tareas) == 1

def test_eliminar_tarea(agregar_tarea):
    tareas.eliminar_tarea(tareas.tareas[0])
    with pytest.raises(KeyError):
        existe = tareas.tareas[0]

def test_editar_titulo_tarea(agregar_tarea):
    tareas.editar_campo(tareas.tareas[0], "titulo", "valor_nuevo")
    assert tareas.tareas[0]["titulo"] == "valor_nuevo"

def test_avanzar_estado_tarea(agregar_tarea):
    tareas.editar_campo(tareas.tareas[0], "estado", "")
    assert tareas.tareas[0]["estado"] == "progreso"
    tareas.editar_campo(tareas.tareas[0], "estado", "")
    assert tareas.tareas[0]["estado"] == "completada"
    tareas.editar_campo(tareas.tareas[0], "estado", "")
    assert tareas.tareas[0]["estado"] == "completada"

def test_leer_tarea(agregar_tarea):
    assert tareas.tareas[0]["titulo"] == "titulo"
    assert tareas.tareas[0]["descripcion"] == "descripcion"

def test_guardar_y_cargar_tarea(agregar_tarea):
    tareas.guardar_tareas()
    tareas.cargar_tareas()
    assert tareas.tareas[0]

def test_parse_fecha_correcta():
    tareas.parse_fecha("2020-1-2")

def test_parse_fecha_incorrecta():
    with pytest.raises(ValueError):
        tareas.parse_fecha("1990-0-1")
    with pytest.raises(ValueError):
        tareas.parse_fecha("2020/1/2")
    with pytest.raises(ValueError):
        tareas.parse_fecha("jfiosd")
    with pytest.raises(ValueError):
        tareas.parse_fecha("")

def test_contra_incorrecta(auth):
    with pytest.raises(InvalidToken):
        tareas.init("user", "pass_incorrecta")

pytest.main()