
import tkinter as tk
import interfaz
import gestor_contactos as gestor

def main():
    
    ventana = tk.Tk()

    interfaz.crear_interfaz(ventana, gestor)

    ventana.mainloop()

if __name__ == "__main__":
    main()