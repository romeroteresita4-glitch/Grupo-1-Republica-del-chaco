import os 
import csv

RUTA_ARCHIVO = os.path.join(os.path.dirname(__file__), "contactos.csv")

def cargar_contactos():
    if not os.path.exists(RUTA_ARCHIVO):
        return []
    with open(RUTA_ARCHIVO, mode="r", newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        return list(lector)

def guardar_contactos():
    with open(RUTA_ARCHIVO, mode="w", newline="", encoding="utf-8") as f:
        campos = ["nombre", "apellido", "telefono", "email"]
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(contactos)

contactos = cargar_contactos()

def agregar_contacto(nombre, apellido, telefono, email):
    existente = buscar_contacto(nombre, apellido)
    if existente:
        existente["telefono"] = telefono
        existente["email"] = email
    else:
        contacto = {"nombre": nombre, "apellido": apellido, "telefono": telefono, "email": email}
        contactos.append(contacto)
    guardar_contactos()

def buscar_contacto(nombre, apellido):
    for c in contactos:
        if c["nombre"].lower() == nombre.lower() and c["apellido"].lower() == apellido.lower():
            return c
    return None

def buscar_contactos(busqueda):
    resultados_busqueda = [
        c for c in contactos 
        if busqueda in c['nombre'].lower() 
        or busqueda in c['apellido'].lower()
        or busqueda in c['email'].lower() 
        or busqueda in c['telefono'].lower()
    ]
    if resultados_busqueda:
        return resultados_busqueda
    return 'Vacio'

def eliminar_contacto(nombre, apellido):
    global contactos
    contactos = [c for c in contactos if not (c['nombre'] == nombre and c['apellido'] == apellido)]
    guardar_contactos()

def obtener_todos(resultados_busqueda=None):
    if not resultados_busqueda:
        return contactos
    elif resultados_busqueda == 'Vacio':
        return []
    return resultados_busqueda