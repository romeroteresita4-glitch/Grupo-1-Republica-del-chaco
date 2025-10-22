# gestor_contactos.py
# -------------------
# Módulo encargado de manejar la lógica de los contactos:
# agregar, buscar, eliminar y obtener todos.

# Lista global donde se guardan los contactos
contactos = []

contactos.extend([
    {'nombre': 'Juan', 'apellido': 'Alonso', 'email': 'juan@ejemplo.com', 'telefono': '3644242523'},
    {'nombre': 'Pedro', 'apellido': 'Araujo', 'email': 'pedrito@hotmail.com', 'telefono': '3644202542'},
    {'nombre': 'Juana', 'apellido': 'Araujo', 'email': 'juanaaraujo@gmail.com', 'telefono': '1124202523'},
    {'nombre': 'Maria', 'apellido': 'Lopez', 'email': 'marial@ejemplo.com', 'telefono': '3624299523'},
    {'nombre': 'Susana', 'apellido': 'Diaz', 'email': 'susana@gmail.com', 'telefono': '1144212323'}
])

def agregar_contacto(nombre, apellido, telefono, email):
    """
    Agrega un nuevo contacto al listado.
    Si el contacto ya existe (mismo nombre y apellido), lo actualiza.
    """
    existente = buscar_contacto(nombre, apellido)
    if existente:
        existente["telefono"] = telefono
        existente["email"] = email
    else:
        contacto = {"nombre": nombre, "apellido": apellido, "telefono": telefono, "email": email}
        contactos.append(contacto)

def buscar_contacto(nombre, apellido):
    """
    Busca un contacto por nombre y apellido (sin distinguir mayúsculas/minúsculas).
    Devuelve el diccionario del contacto o None si no existe.
    """
    for c in contactos:
        if c["nombre"].lower() == nombre.lower() and c["apellido"].lower() == apellido.lower():
            return c
    return None

def buscar_contactos(busqueda):
    """
    Busca contactos que coincidan con el texto de búsqueda en cualquier campo.
    """
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
    """
    Elimina un contacto por nombre y apellido.
    """
    global contactos
    contactos = [c for c in contactos if not (c['nombre'] == nombre and c['apellido'] == apellido)]

def obtener_todos(resultados_busqueda=None):
    """
    Devuelve una lista de todos los contactos actuales.
    """
    if not resultados_busqueda:
        return contactos
    elif resultados_busqueda == 'Vacio':
        return []
    return resultados_busqueda