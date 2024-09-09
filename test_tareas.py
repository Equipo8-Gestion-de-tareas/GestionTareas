import pytest
from datetime import datetime
import tareas

@pytest.fixture
def auth():
    tareas.init("user", "pass-hash")

@pytest.fixture
def add_test(auth):
    tareas.agregar_tarea("titulo", "descripcion", datetime.now(), "etiqueta")

def test_tarea_agregada(add_test):
    assert len(tareas.tareas) == 1

pytest.main()