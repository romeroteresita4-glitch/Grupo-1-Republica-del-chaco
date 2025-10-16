# main.py
# --------
# Punto de inicio del programa.
# Crea la ventana principal, carga la interfaz y ejecuta el bucle principal.

import tkinter as tk
import interfaz
import gestor_contactos as gestor

def main():
    """Función principal que inicia la aplicación."""
    # Crear la ventana raíz
    ventana = tk.Tk()

    # Crear la interfaz dentro de la ventana, pasando el gestor de contactos
    interfaz.crear_interfaz(ventana, gestor)

    # Iniciar el bucle principal (loop de la app)
    ventana.mainloop()

# Ejecutar solo si se llama directamente (no si se importa)
if __name__ == "__main__":
    main()