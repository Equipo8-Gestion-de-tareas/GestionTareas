import json, base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Style
from pymenu import Menu
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO, filename="logs.txt", format="%(asctime)s [%(levelname)s] - %(message)s")
log = logging.getLogger(__name__)

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
    log.info("Cargado datos del usuario")

def input_fecha_ui(mensaje: str, permitir_vacio: bool = False) -> datetime:
    incorrecto = True
    while incorrecto:
        try:
            fecha = input(mensaje)
            if not fecha and permitir_vacio:
                return None
            fecha = parse_fecha(fecha)
            incorrecto = False
        except ValueError:
            logging.warning("Input de fecha incorrecto del usuario")
            print(Fore.RED + "Formato incorrecto, por favor reintentar." + Style.RESET_ALL)
    return fecha

def get_tarea_por_id_ui():
    incorrecto = True
    while incorrecto:
        try:
            id = int(input("Ingrese ID de tarea: "))
            tarea = tareas[id]
            incorrecto = False
        except ValueError:
            logging.warning("Input de ID incorrecto del usuario")
            print(Fore.RED + "ID incorrecto, por favor reintentar." + Style.RESET_ALL)
        except KeyError:
            logging.warning("Usuario intenta acceder tarea inexistente")
            print(Fore.RED + "ID no existe, por favor reintentar." + Style.RESET_ALL)
    return tarea

def editar_campo_ui(campo: str, tarea):
    match campo:
        case "titulo":
            nuevo = input("Ingrese nuevo título: ")
        case "descripcion":
            nuevo = input("Ingrese nueva descripción")
        case "fecha_vencimiento":
            nuevo = input_fecha_ui("Ingrese nueva fecha de vencimiento: ")
        case "etiqueta":
            nuevo = input("Ingrese nueva etiqueta")
        case "estado":
            nuevo = input("Enter para avanzar estado de progreso.")
    editar_campo(tarea, campo, nuevo)
    menu_principal()

def editar_tarea_ui():
    tarea = get_tarea_por_id_ui()
    menu_edit = Menu(f"Elegir campo a editar en tarea {tarea['id']}")
    menu_edit.add_options([
    ("Título", lambda: editar_campo_ui("titulo", tarea)),
    ("Descripción", lambda: editar_campo_ui("descripcion", tarea)),
    ("Fecha de vencimiento", lambda: editar_campo_ui("fecha_vencimiento", tarea)),
    ("Etiqueta", lambda: editar_campo_ui("etiqueta", tarea)),
    ("Estado de progreso", lambda: editar_campo_ui("estado", tarea)),
    ("Volver", menu_principal)
    ])
    menu_edit.show()

def agregar_tarea_ui():
    titulo = input("Ingrese título: ")
    desc = input("Ingrese descripción: ")
    fecha_vencimiento = input_fecha_ui("Ingrese fecha de vencimiento [YYYY-mm-dd]: ")
    etiqueta = input("Ingrese etiqueta: ")
    agregar_tarea(titulo, desc, fecha_vencimiento, etiqueta)
    menu_principal()

def mostrar_tareas_ui():
    if len(tareas) == 0:
        print("No hay tareas.")
    for tarea in tareas.values():
        print_tarea(tarea)
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

def resultado_rango_fechas_ui():
    print("Dejar campo vacío para rango abierto.")
    antes = input_fecha_ui("Tareas antes de [YYY-mm-dd]: ", permitir_vacio = True)
    desp = input_fecha_ui("Tareas después de [YYY-mm-dd]: ", permitir_vacio = True)
    tareas = buscar_rango_tareas(antes, desp)
    for t in tareas:
        print_tarea(t)
    input("Enter para continuar.")
    menu_principal()

def buscar_tarea_ui():
    menu_busqueda = Menu("Elegir criterio de búsqueda")
    menu_busqueda.add_options([
    ("Título", lambda: resultado_busqueda_ui("titulo")),
    ("Descripción", lambda: resultado_busqueda_ui("descripcion")),
    ("Rango de fechas", lambda: resultado_rango_fechas_ui()),
    ("Etiqueta", lambda: resultado_busqueda_ui("etiqueta")),
    ("Estado de progreso", lambda: resultado_busqueda_ui("estado")),
    ("Volver", menu_principal)
    ])
    menu_busqueda.show()

def buscar_rango_tareas(antes_de: datetime, despues_de: datetime):
    if not antes_de:
        antes_de = datetime.max
    if not despues_de:
        despues_de = datetime.min
    global tareas
    res = []
    for id, tarea in tareas.items():
        fecha = parse_fecha(tarea["fecha_vencimiento"])
        if despues_de < fecha < antes_de:
            res.append(tarea)
    return res

def parse_fecha(fecha: str) -> datetime:
    return datetime.strptime(fecha, "%Y-%m-%d")

def print_tarea(tarea):
    print(f'\n[ID {tarea["id"]}]')
    print(f'  Título: {tarea["titulo"]}')
    print(f'  Descripción: {tarea["descripcion"]}')
    print(f'  Fecha de vencimiento: {tarea["fecha_vencimiento"]}')
    print(f'  Etiqueta: {tarea["etiqueta"]}')
    if(parse_fecha(tarea["fecha_vencimiento"]) < datetime.now()):
        print(Fore.RED + "ATRASADA" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "A tiempo" + Style.RESET_ALL)
    match tarea["estado"]:
        case "pendiente":
            print( "Estado: " + Fore.YELLOW + "Pendiente" + Style.RESET_ALL)
        case "progreso":
            print( "Estado: " + Fore.LIGHTBLUE_EX + "En progreso" + Style.RESET_ALL)
        case "completada":
            print( "Estado: " + Fore.LIGHTGREEN_EX + "Completada" + Style.RESET_ALL)
    print("")


def agregar_tarea(titulo: str, descripcion: str, fecha_vencimiento: datetime, etiqueta: str):
    global tareas
    tarea = {}
    tarea["titulo"] = titulo
    tarea["descripcion"] = descripcion
    tarea["fecha_vencimiento"] = fecha_vencimiento.strftime("%Y-%m-%d")
    tarea["etiqueta"] = etiqueta
    tarea["estado"] = "pendiente"
    if not tareas:
        tarea["id"] = 0
        tareas[0] = tarea
        return
    ultimo_id = list(tareas.keys())[-1]
    id = ultimo_id + 1
    tareas[id] = tarea
    tarea["id"] = id
    logging.info("Tarea nueva agregada")
    guardar_tareas()

def editar_campo(tarea, campo: str, valor):
    if campo == "estado":
        if tarea[campo] == "pendiente":
            tarea[campo] = "progreso"
        elif tarea[campo] == "progreso":
            tarea[campo] = "completada"
        else:
            log.warning("Usuario intenta avanzar tarea completada")
    elif isinstance(valor, datetime):
        tarea[campo] = valor.strftime("%Y-%m-%d")
    else:
        tarea[campo] = valor
    logging.info(f"Tarea {tarea['id']} editada")
    guardar_tareas()

def get_tareas_by(criterio: str, valor: str):
    global tareas
    res = []
    for id, tarea in tareas.items():
        if valor.lower() in tarea[criterio].lower():
            res.append(tarea)
    return res

def guardar_tareas():
    global tareas
    json_tareas = json.dumps(tareas)
    if json_tareas == "":
        json_tareas = "{}"
    encryp = f.encrypt(bytes(json_tareas, encoding="utf-8"))
    with open("./db/tareas-"+usr+".enc", "w") as file:
        log.info("Tareas encriptadas y guardadas")
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
        log.warning("Excepcion esperada, archivo de datos guardado no encontrado, creando archivo")
        new = open("./db/tareas-"+usr+".enc", "w")
        new.close()
        return
    encryp = bytes(encryp, encoding="utf-8")
    dec = f.decrypt(encryp).decode("utf-8")
    tareas = json.loads(dec, object_hook=_int_keys)

def salir():
    guardar_tareas()
    log.info("Aplicacion cerrada")
    quit()

menu = Menu("Gestión de tareas")
menu.add_options([
    ("Agregar tarea", agregar_tarea_ui),
    ("Mostrar todas las tareas", mostrar_tareas_ui),
    ("Buscar tareas", buscar_tarea_ui),
    ("Editar tarea por ID", editar_tarea_ui),
    ("Salir", salir)
])

def menu_principal():
    menu.show()

def init(name: str, passw: str):
    set_user_data(name, passw)
    cargar_tareas()
    guardar_tareas()
    menu_principal()

init("woww", "woww")