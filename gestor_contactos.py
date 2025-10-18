# gestor_contactos.py
# -------------------
# Módulo encargado de manejar la lógica de los contactos:
# agregar, buscar, eliminar y obtener todos.

# Lista global donde se guardan los contactos
contactos = []

contactos.extend([{'nombre':'Juan Alonso','email':'juan@ejemplo.com','telefono':'3644242523'},
                 {'nombre':'Pedro Araujo','email':'pedrito@hotmail.com','telefono':'3644202542'},
                 {'nombre':'Juana Araujo','email':'juanaaraujo@gmail.com','telefono':'1124202523'},
                 {'nombre':'Maria Lopez','email':'marial@ejemplo.com','telefono':'3624299523'},
                 {'nombre':'Susana Diaz','email':'susana@gmail.com','telefono':'1144212323'}])

def agregar_contacto(nombre, telefono, email):
    """
    Agrega un nuevo contacto al listado.
    Si el contacto ya existe (mismo nombre), lo actualiza.
    """
    existente = buscar_contacto(nombre)
    if existente:
        existente["telefono"] = telefono
        existente["email"] = email
    else:
        contacto = {"nombre": nombre, "telefono": telefono, "email": email}
        contactos.append(contacto)

def buscar_contacto(nombre):
    """
    Busca un contacto por nombre (sin distinguir mayúsculas/minúsculas).
    Devuelve el diccionario del contacto o None si no existe.
    """
    for c in contactos:
        if c["nombre"].lower() == nombre.lower():
            return c
    return None

def eliminar_contacto(nombre):
    """
    Elimina un contacto por nombre.
    """
    global contactos
    contactos = [c for c in contactos if c["nombre"].lower() != nombre.lower()]

def obtener_todos():
    """
    Devuelve una lista de todos los contactos actuales.
    """
    return contactos