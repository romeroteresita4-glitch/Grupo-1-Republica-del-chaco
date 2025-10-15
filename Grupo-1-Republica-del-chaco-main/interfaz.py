import tkinter as tk
from tkinter import messagebox
import gestor_contactos as gc

def agregar():
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    email = entry_email.get()
    if nombre and telefono:
        gc.agregar_contacto(nombre, telefono, email)
        actualizar_lista()
        limpiar_campos()
    else:
        messagebox.showwarning("Atención", "Nombre y teléfono son obligatorios.")

def buscar():
    nombre = entry_nombre.get()
    contacto = gc.buscar_contacto(nombre)
    if contacto:
        messagebox.showinfo("Contacto encontrado", f"📇 {contacto}")
    else:
        messagebox.showinfo("Sin resultados", "No se encontró el contacto.")

def eliminar():
    nombre = entry_nombre.get()
    gc.eliminar_contacto(nombre)
    actualizar_lista()
    limpiar_campos()

def actualizar_lista():
    listbox.delete(0, tk.END)
    for c in gc.obtener_todos():
        listbox.insert(tk.END, f"{c['nombre']} - {c['telefono']} - {c['email']}")

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Contactos")

tk.Label(ventana, text="Nombre:").grid(row=0, column=0)
tk.Label(ventana, text="Teléfono:").grid(row=1, column=0)
tk.Label(ventana, text="Email:").grid(row=2, column=0)

entry_nombre = tk.Entry(ventana)
entry_telefono = tk.Entry(ventana)
entry_email = tk.Entry(ventana)

entry_nombre.grid(row=0, column=1)
entry_telefono.grid(row=1, column=1)
entry_email.grid(row=2, column=1)

tk.Button(ventana, text="Agregar", command=agregar).grid(row=3, column=0)
tk.Button(ventana, text="Buscar", command=buscar).grid(row=3, column=1)
tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=3, column=2)

listbox = tk.Listbox(ventana, width=50)
listbox.grid(row=4, column=0, columnspan=3, pady=10)

ventana.mainloop()
