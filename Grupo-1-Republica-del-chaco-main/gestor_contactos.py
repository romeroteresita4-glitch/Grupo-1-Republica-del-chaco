contactos = []

def agregar_contacto(nombre, telefono, email):
    contacto = {"nombre": nombre, "telefono": telefono, "email": email}
    contactos.append(contacto)

def buscar_contacto(nombre):
    for c in contactos:
        if c["nombre"].lower() == nombre.lower():
            return c
    return None

def eliminar_contacto(nombre):
    global contactos
    contactos = [c for c in contactos if c["nombre"].lower() != nombre.lower()]

def obtener_todos():
    return contactos
