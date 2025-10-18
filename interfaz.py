# interfaz.py
# ------------
# Contiene la definición de la interfaz gráfica del Gestor de Contactos.
# No contiene lógica de negocio ni el bucle principal (eso está en main.py).

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Para Treeview (tabla con columnas)

def crear_interfaz(ventana, gestor):
    """
    Crea la interfaz gráfica dentro de una ventana Tk existente.

    Parámetros:
    - ventana: objeto Tk principal (creado en main.py)
    - gestor: módulo o clase que contiene funciones de manejo de contactos
              (agregar_contacto, buscar_contacto, eliminar_contacto, obtener_todos)
    """

    # === FUNCIONES INTERNAS DE LA INTERFAZ ===
    def agregar():
        """Agrega un nuevo contacto usando los datos del formulario."""
        nombre = entry_nombre.get()
        telefono = entry_telefono.get()
        email = entry_email.get()
        if nombre and telefono:
            gestor.agregar_contacto(nombre, telefono, email)
            actualizar_lista()
            ordenar_tabla(tree, columns[0], False)
            limpiar_campos()
        else:
            messagebox.showwarning("Atención", "Nombre y teléfono son obligatorios.")

    def buscar():
        """Busca un contacto por nombre y muestra el resultado."""
        nombre = entry_nombre.get()
        contacto = gestor.buscar_contacto(nombre)
        if contacto:
            messagebox.showinfo(
                "Contacto encontrado",
                f"📇 Nombre: {contacto['nombre']}\n📞 Teléfono: {contacto['telefono']}\n✉️ Email: {contacto['email']}"
            )
        else:
            messagebox.showinfo("Sin resultados", "No se encontró el contacto.")

    def eliminar():
        """Elimina el contacto con el nombre indicado."""
        nombre = entry_nombre.get()
        gestor.eliminar_contacto(nombre)
        actualizar_lista()
        ordenar_tabla(tree, columns[0], False)
        limpiar_campos()

    def actualizar_lista():
        """Actualiza la lista de contactos mostrada en pantalla."""
        for item in tree.get_children():
            tree.delete(item)
        for c in gestor.obtener_todos():
            tree.insert("", "end", values=(c['nombre'], c['telefono'], c['email']))

    def limpiar_campos():
        """Limpia los campos de texto del formulario."""
        entry_nombre.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_email.delete(0, tk.END)

    # se utiliza para ordenar los contactos según la preferencia del usuario
    def ordenar_tabla(treeview, col, reverse):
        # Obtener todos los datos
        data = [(treeview.set(k, col), k) for k in treeview.get_children('')]

        # Para que ordene números como números y no como strings
        try:
            data.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0].lower(), reverse=reverse)

        # Reordenar en el treeview
        for index, (val, k) in enumerate(data):
            treeview.move(k, '', index)

        # Cambiar el encabezado para indicar la dirección del orden
        treeview.heading(col, command=lambda _col=col, _rev=not reverse: ordenar_tabla(treeview, _col, _rev))


    # === ELEMENTOS GRÁFICOS ===
    ventana.title("Gestor de Contactos")
    ventana.minsize(500, 300)

    # Para dar otro estilo a la tabla a la ventana
    style = ttk.Style(ventana)
    style.theme_use("clam")

    # Etiquetas
    tk.Label(ventana, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    tk.Label(ventana, text="Teléfono:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    tk.Label(ventana, text="Email:").grid(row=2, column=0, sticky="e", padx=5, pady=5)

    # Campos de texto
    entry_nombre = tk.Entry(ventana)
    entry_telefono = tk.Entry(ventana)
    entry_email = tk.Entry(ventana)
    entry_nombre.grid(row=0, column=1, sticky="we", padx=5, pady=5)
    entry_telefono.grid(row=1, column=1, sticky="we", padx=5, pady=5)
    entry_email.grid(row=2, column=1, sticky="we", padx=5, pady=5)

    # Botones
    tk.Button(ventana, text="Agregar", command=agregar).grid(row=3, column=0, sticky="we", padx=5, pady=5)
    tk.Button(ventana, text="Buscar", command=buscar).grid(row=3, column=1, sticky="we", padx=5, pady=5)
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=3, column=2, sticky="we", padx=5, pady=5)

    # === Treeview para mostrar contactos (tipo tabla Excel) ===
    columns = ("Nombre", "Teléfono", "Email")
    tree = ttk.Treeview(ventana, columns=columns, show="headings")
    tree.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
    
    # Ordena la tabla cuando el usuario presiona sobre el encabezado de una columna
    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: ordenar_tabla(tree, _col, False))
    
    # Cargar lista inicial
    actualizar_lista()

    # Ordena la tabla al iniciar por la primer columna de forma ascendente
    ordenar_tabla(tree, columns[0], False)

    # Scroll vertical
    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=4, column=3, sticky="ns")

    # === CONFIGURACIÓN RESPONSIVA ===
    # Columnas de la ventana se expanden proporcionalmente
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=2)
    ventana.grid_columnconfigure(2, weight=1)
    ventana.grid_rowconfigure(4, weight=1)  # la tabla crece verticalmente

    

