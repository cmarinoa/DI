import tkinter as tk
from tkinter import messagebox

def nueva_ventana():
    messagebox.showinfo("Nuevo", "Abrir una nueva ventana")

def salir_app():
    root.quit()

def acerca_de():
    messagebox.showinfo("Acerca de", "miau")

root = tk.Tk()
root.title("Ejercicio 9: Menú")
root.geometry("300x150")

menu_principal = tk.Menu(root)
root.config(menu=menu_principal)

menu_archivo = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Nuevo", command=nueva_ventana)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=salir_app)

menu_acerca_de = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Acerca de", menu=menu_acerca_de)
menu_acerca_de.add_command(label="Acerca de", command=acerca_de)

root.mainloop()