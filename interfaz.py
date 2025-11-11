# interfaz.py
# Contiene la definición de la interfaz gráfica del Gestor de Contactos.
# No contiene lógica de negocio ni el bucle principal (eso está en main.py).

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Para Treeview (tabla con columnas)
import re # para la funcion match para comparar el email con el patrón válido

# Crea la interfaz gráfica dentro de una ventana Tk existente.
def crear_interfaz(ventana, gestor):
    
    # funcion de validación de email
    def email_valido(email):
        # Regex básico para validar email
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email) is not None

    # === FUNCIONES INTERNAS DE LA INTERFAZ ===

    # Agrega un nuevo contacto usando los datos del formulario.
    def agregar():
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        telefono = entry_telefono.get().strip()
        email = entry_email.get().strip()
        
        if not nombre or not apellido or not telefono:
            messagebox.showwarning("Atención", "Nombre, apellido y teléfono son obligatorios.")
            return
        
        if email and not email_valido(email):
            messagebox.showerror("Email inválido", "Por favor, ingresa un email con formato válido.")
            return

        gestor.agregar_contacto(nombre, apellido, telefono, email)
        buscar_en_tabla()
        limpiar_campos()

    # Busca contactos que coincidan con el campo de búsqueda.
    def buscar():
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        telefono = entry_telefono.get().strip()
        email = entry_email.get().strip()
        
        # Verifica que al menos un campo tenga datos.
        if not any([nombre, apellido, telefono, email]):
            messagebox.showwarning("Atención", "Ingresa al menos un dato para buscar.")
            return
        
        # Busca según el campo que tenga contenido.
        resultados = []
        if nombre:
            resultados = [c for c in gestor.obtener_todos() if nombre.lower() in c['nombre'].lower()]
        elif apellido:
            resultados = [c for c in gestor.obtener_todos() if apellido.lower() in c['apellido'].lower()]
        elif telefono:
            resultados = [c for c in gestor.obtener_todos() if telefono in c['telefono']]
        elif email:
            resultados = [c for c in gestor.obtener_todos() if email.lower() in c['email'].lower()]
        
        # Muestra los resultados en ventana personalizada.
        if resultados:
            # Crear ventana personalizada.
            ventana_resultado = tk.Toplevel(ventana)
            ventana_resultado.title("Resultado de búsqueda")
            ventana_resultado.configure(bg='#F9FAFB')
            ventana_resultado.geometry("500x300")
            
            # Frame con scrollbar.
            frame_principal = tk.Frame(ventana_resultado, bg='#F9FAFB')
            frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Texto con scrollbar.
            scrollbar_resultado = tk.Scrollbar(frame_principal)
            scrollbar_resultado.pack(side="right", fill="y")
            
            texto_resultado = tk.Text(
                frame_principal, 
                wrap="word", 
                font=('Segoe UI', 13),
                bg='#FFFFFF',
                fg='#333333',
                yscrollcommand=scrollbar_resultado.set,
                relief='flat',
                padx=15,
                pady=15
            )
            texto_resultado.pack(side="left", fill="both", expand=True)
            scrollbar_resultado.config(command=texto_resultado.yview)
            
            # Preparar contenido.
            if len(resultados) == 1:
                c = resultados[0]
                contenido = f"☺  {c['nombre']}, {c['apellido']}\n✆  {c['telefono']}\n✉  {c['email']}"
            else:
                contenido = f"Se encontraron {len(resultados)} contactos:\n\n"
                for c in resultados:
                    contenido += f"☺  {c['nombre']}, {c['apellido']}\n✆  {c['telefono']}\n✉  {c['email']}\n\n"
            
            texto_resultado.insert("1.0", contenido)
            texto_resultado.config(state="disabled")  # Solo lectura
            
            # Botón cerrar.
            tk.Button(
                ventana_resultado, 
                text="Cerrar", 
                command=ventana_resultado.destroy,
                bg='#03A9F4',
                fg='white',
                font=('Segoe UI', 12),
                padx=20,
                pady=5
            ).pack(pady=10)
            
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron contactos con ese criterio.")

    # Busqueda automática en tabla.
    def buscar_en_tabla():
        busqueda = entry_buscar.get().strip().lower()

        # Si el input buscar está vacío muesta todos los contactos.
        if not busqueda:
            actualizar_lista()
            ordenar_tabla(tree, columns[0], False) 
            return
        
        # Si el input no está vacío busca contactos que coincidan con la búsqueda.
        resultados_busqueda = gestor.buscar_contactos(busqueda)
        actualizar_lista(resultados_busqueda)
        ordenar_tabla(tree, columns[0], False)
    
    # Elimina al contacto seleccionado.
    def eliminar():      
        contacto = tree.selection()
        if not contacto:
            messagebox.showwarning("Selecciona", "Debes seleccionar un contacto para eliminar.")
            return
        
        valores = tree.item(contacto)['values']
        nombre = valores[0]
        apellido = valores[1]
        
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar al contacto {nombre} {apellido}?")
        if confirm:
            gestor.eliminar_contacto(nombre, apellido)
            buscar_en_tabla()
        
    # Actualiza la lista de contactos en la tabla.
    def actualizar_lista(resultados_busqueda=None):
        for item in tree.get_children():
            tree.delete(item)
        for c in gestor.obtener_todos(resultados_busqueda):
            tree.insert("", "end", values=(c['nombre'], c['apellido'], c['telefono'], c['email']))

    # Limpia los campos de texto del formulario.
    def limpiar_campos():
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        
    # Se utiliza para ordenar los contactos según la columna de preferencia del usuario.
    def ordenar_tabla(treeview, col, reverse):
        # Obtiene todos los datos.
        data = [(treeview.set(k, col), k) for k in treeview.get_children('')]

        # Para que ordene números como números y no como strings.
        try:
            data.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0].lower(), reverse=reverse)

        # Reordena en el treeview
        for index, (val, k) in enumerate(data):
            treeview.move(k, '', index)

        # Limpia flechas de todos los encabezados.
        for c in treeview["columns"]:
            treeview.heading(c, text=c)

        # Agrega flecha al encabezado de la columna ordenada.
        flecha = "▲" if not reverse else "▼"
        treeview.heading(col, text=f"{col.center(10)}{flecha}")

        # Cambia el encabezado para invertir la dirección al hacer clic.
        treeview.heading(col, command=lambda _col=col, _rev=not reverse: ordenar_tabla(treeview, _col, _rev))


    # === ELEMENTOS GRÁFICOS ===
    ventana.title("Gestor de Contactos")
    ventana.minsize(600, 400)
    ventana.configure(bg='#F9FAFB') # Fondo principal de la ventana


    # Para dar otro estilo a la tabla a la ventana.
    style = ttk.Style(ventana)
    style.theme_use("clam")

    # Etiquetas
    tk.Label(ventana, text="Nombre:", bg='#F9FAFB', fg='#333333', font=('Segoe UI', 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
    tk.Label(ventana, text="Apellido:", bg='#F9FAFB', fg='#333333', font=('Segoe UI', 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    tk.Label(ventana, text="Teléfono:", bg='#F9FAFB', fg='#333333', font=('Segoe UI', 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    tk.Label(ventana, text="Email:", bg='#F9FAFB', fg='#333333', font=('Segoe UI', 10)).grid(row=3, column=0, sticky="e", padx=5, pady=5)

    # Campos de texto
    entry_nombre = tk.Entry(ventana, bg="#FFFFFF", fg="#333333", highlightbackground="#CCCCCC", highlightthickness=1, font=('Segoe UI', 10))
    entry_apellido = tk.Entry(ventana, bg="#FFFFFF", fg="#333333", highlightbackground="#CCCCCC", highlightthickness=1, font=('Segoe UI', 10))
    entry_telefono = tk.Entry(ventana, bg="#FFFFFF", fg="#333333", highlightbackground="#CCCCCC", highlightthickness=1, font=('Segoe UI', 10))
    entry_email = tk.Entry(ventana, bg="#FFFFFF", fg="#333333", highlightbackground="#CCCCCC", highlightthickness=1, font=('Segoe UI', 10))
    entry_nombre.grid(row=0, column=1, sticky="we", padx=5, pady=5)
    entry_apellido.grid(row=1, column=1, sticky="we", padx=5, pady=5)
    entry_telefono.grid(row=2, column=1, sticky="we", padx=5, pady=5)
    entry_email.grid(row=3, column=1, sticky="we", padx=5, pady=5)

    # Botones
    tk.Button(ventana, text="Agregar", command=agregar, bg='#4CAF50', fg='white', activebackground='#66BB6A', relief='raised', borderwidth=1, font=('Segoe UI', 10)).grid(row=4, column=0, sticky="we", padx=5, pady=5)
    tk.Button(ventana, text="Buscar", command=buscar, bg='#03A9F4', fg='white', activebackground='#29B6F6', relief='raised', borderwidth=1, font=('Segoe UI', 10)).grid(row=4, column=1, sticky="we", padx=5, pady=5)
    tk.Button(ventana, text="Limpiar", command=limpiar_campos, bg='#F5B027', fg='white', activebackground='#F7C453', relief='raised', borderwidth=1, font=('Segoe UI', 10)).grid(row=4, column=2, sticky="we", padx=5, pady=5)
    tk.Button(ventana, text="Eliminar", command=eliminar, bg='#F44336', fg='white', activebackground='#EF5350', relief='raised', borderwidth=1, font=('Segoe UI', 10)).grid(row=7, column=2, sticky="we", padx=5, pady=5)

    # Buscar en tabla
    tk.Label(ventana, text="Filtrar: ", bg='#F9FAFB', fg='#333333', font=('Segoe UI', 10)).grid(row=5, column=0, sticky="e", padx=5, pady=5)
    entry_buscar = tk.Entry(ventana, width=40, bg="#FFFFFF", fg="#333333", highlightbackground="#CCCCCC", highlightthickness=1, font=('Segoe UI', 10))
    entry_buscar.grid(row=5, column=1, sticky="w", padx=5, pady=5)
    entry_buscar.bind("<KeyRelease>", lambda event: buscar_en_tabla())

    # === Treeview para mostrar contactos (tipo tabla Excel) ===
    columns = ("Nombre", "Apellido", "Teléfono", "Email")
    tree = ttk.Treeview(ventana, columns=columns, show="headings")
    tree.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
    
    # Configurar ancho de columnas
    tree.column("Nombre", width=120)
    tree.column("Apellido", width=120)
    tree.column("Teléfono", width=120)
    tree.column("Email", width=200)
    
    # Configuración del estilo para el CUERPO de la tabla
    style.configure("Treeview", background="#FFFFFF", foreground="#333333", font=('Segoe UI', 10))
    # Configuración del estilo del elemento seleccionado de la tabla
    style.map("Treeview", background=[('selected', '#E0F7FA')], foreground=[('selected', '#000000')])
    # Configuración del estilo para el ENCABEZADO de la tabla (Treeview.Heading)
    style.configure("Treeview.Heading", background="#F9FAFB", foreground="#212121", font=('Segoe UI', 10, 'bold'))
    
    # Ordena la tabla cuando el usuario presiona sobre el encabezado de una columna.
    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: ordenar_tabla(tree, _col, False))
    
    # Cargar lista inicial.
    actualizar_lista()

    # Ordena la tabla al iniciar por la primer columna de forma ascendente.
    ordenar_tabla(tree, columns[0], False)

    # Scroll vertical
    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=6, column=3, sticky="ns")
    

    # === CONFIGURACIÓN RESPONSIVA ===
    # Columnas de la ventana se expanden proporcionalmente
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=2)
    ventana.grid_columnconfigure(2, weight=1)
    ventana.grid_rowconfigure(6, weight=1)  # la tabla crece verticalmente