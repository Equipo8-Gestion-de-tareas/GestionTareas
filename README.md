# Tarea 1 - Pruebas de Software

Equipo 8:

- Benjamín Saez
- Tomás Guttman

---

## Descripción

Aplicación de consola de gestión de tareas implementada en Python.

El proyecto consta del desarrollo de una aplicación de gestión de tareas que, a través de la línea de comandos, permite a los usuarios crear, consultar, actualizar y eliminar tareas, las que deben tener un título, una descripción, una fecha de vencimiento, una etiqueta y un estado.

Además, debe incluir una funcionalidad de búsqueda de tareas que pueda ser filtrada en función de los atributos de las tareas, y un sistema de gestión de estados para cambiar el estado de las tareas.

La aplicación deberá tener autenticación para su acceso mediante un nombre de usuario y una contraseña.

La ejecución de la aplicación, así como su almacenamiento y sistema de autenticación, funcionarán de manera local en un computador.

## Instalación

Abra una consola en la raiz del proyecto y siga los siguientes pasos:

1. Cree un entorno virtual: `python -m venv env`.

2. Inicie el entorno virtual: `.\env\Scripts\activate`.

3. Instale las dependencias: `pip install -r requirements.txt`.

4. Ejecute el script `init.py` para la inicialización de archivos: `python init.py`.

## Cómo usar

- Para correr la aplicación verifique que la última línea del archivo `index.py` (llamado a la función main) **no esté comentada** y ejecute el script.
- Para ejecutar las pruebas, verifique que la última línea del archivo `index.py` (llamado a la función main) **esté comentada** y ejecute en la consola:
  - `pytest -v` para ejecutar todas las pruebas.
  - `pytest -v test_index.py` para ejecutar las pruebas de signin y login.
  - `pytest -v test_tareas.py` para ejecutar las pruebas del resto de funcionalidades de la aplicación.

## Cómo contribuir

Cree un pull request en el repositorio de GitHub.

## Licencia

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
