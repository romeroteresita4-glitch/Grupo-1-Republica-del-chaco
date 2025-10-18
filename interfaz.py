# interfaz.py
# ------------
# Contiene la definición de la interfaz gráfica del Gestor de Contactos.
# No contiene lógica de negocio ni el bucle principal (eso está en main.py).

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Para Treeview (tabla con columnas)
import re # para la funcion match para comparar el email con el patrón válido

def crear_interfaz(ventana, gestor):
    """
    Crea la interfaz gráfica dentro de una ventana Tk existente.

    Parámetros:
    - ventana: objeto Tk principal (creado en main.py)
    - gestor: módulo o clase que contiene funciones de manejo de contactos
              (agregar_contacto, buscar_contacto, eliminar_contacto, obtener_todos)
    """
    # funcion de validación de email
    def email_valido(email):
        # Regex básico para validar email
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email) is not None

    # === FUNCIONES INTERNAS DE LA INTERFAZ ===
    def agregar():
        """Agrega un nuevo contacto usando los datos del formulario."""
        nombre = entry_nombre.get()
        telefono = entry_telefono.get()
        email = entry_email.get()
        if not nombre and not telefono:
            messagebox.showwarning("Atención", "Nombre y teléfono son obligatorios.")
            return
        
        if email and not email_valido(email):
            messagebox.showerror("Email inválido", "Por favor, ingresa un email con formato válido.")
            return

        gestor.agregar_contacto(nombre, telefono, email)
        buscar_en_tabla()

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

    # busqueda automática en tabla
    def buscar_en_tabla():
        busqueda = entry_buscar.get().strip().lower()

        # si el input buscar está vacío muesta todos los contactos
        if not busqueda:
            actualizar_lista()
            ordenar_tabla(tree, columns[0], False) 
            return
        
        # si el input no está vacío busca contactos que coincidan con la búsqueda
        resultados_busqueda= gestor.buscar_contactos(busqueda)
        actualizar_lista(resultados_busqueda)
        ordenar_tabla(tree, columns[0], False)
        
    def eliminar():
        """Elimina el contacto con el nombre indicado."""       
        
        contacto = tree.selection()
        if not contacto:
            messagebox.showwarning("Selecciona", "Debes seleccionar un contacto para eliminar.")
            return
        nombre = tree.item(contacto)['values'][0]
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar al contacto {nombre}?")
        if confirm:
            gestor.eliminar_contacto(nombre)
        buscar_en_tabla()
        
    def actualizar_lista(resultados_busqueda=None):
        """Actualiza la lista de contactos mostrada en pantalla."""
        for item in tree.get_children():
            tree.delete(item)
        for c in gestor.obtener_todos(resultados_busqueda):
            tree.insert("", "end", values=(c['nombre'], c['telefono'], c['email']))

    def limpiar_campos():
        """Limpia los campos de texto del formulario."""
        entry_nombre.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_buscar.delete(0, tk.END)
        
    # se utiliza para ordenar los contactos según la columna de preferencia del usuario
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

        # Limpiar flechas de todos los encabezados
        for c in treeview["columns"]:
            treeview.heading(c, text=c)

        # Agregar flecha al encabezado de la columna ordenada
        flecha = "▲" if not reverse else "▼"
        treeview.heading(col, text=f"{col.center(50)}{flecha}")

        # Cambiar el encabezado para invertir la dirección al hacer clic
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
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=6, column=2, sticky="we", padx=5, pady=5)

    # Buscar en tabla
    tk.Label(ventana, text="Buscar: ").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_buscar = tk.Entry(ventana, width=40)
    entry_buscar.grid(row=4, column=1, sticky="w", padx=5, pady=5)
    entry_buscar.bind("<KeyRelease>", lambda event: buscar_en_tabla())

    # === Treeview para mostrar contactos (tipo tabla Excel) ===
    columns = ("Nombre", "Teléfono", "Email")
    tree = ttk.Treeview(ventana, columns=columns, show="headings")
    tree.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
    
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
    scrollbar.grid(row=5, column=3, sticky="ns")
    

    # === CONFIGURACIÓN RESPONSIVA ===
    # Columnas de la ventana se expanden proporcionalmente
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=2)
    ventana.grid_columnconfigure(2, weight=1)
    ventana.grid_rowconfigure(5, weight=1)  # la tabla crece verticalmente

    

