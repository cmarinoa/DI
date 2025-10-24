import tkinter as tk
from tkinter import messagebox

# Función asociada al menú que muestra el mensaje de "Guardar lista"
def guardar_lista():
    messagebox.showinfo("Guardar Lista", "Lista guardada")

# Función asociada al menú que muestra el mensaje de "Cargar lista"
def cargar_lista():
    messagebox.showinfo("Cargar Lista", "Lista cargada")

# Función asociada al botón de salir de la app
def salir_app():
    root.quit()

# Función para añadir un usuario a la lista
def añadir_usuario():
    nombre = entrada_nombre.get().strip()
    edad = escala_edad.get()
    genero = var_radiobutton.get()

    # Comprobar que el campo "Nombre" no queda vacío
    if not nombre:
        messagebox.showwarning("Advertencia", "Debe ingresar un nombre.")
        return

    # Crear la cadena que se muestra en el listbox y añadirla
    usuario = f"{nombre} - {edad} años - {genero}"
    listbox_usuarios.insert(tk.END, usuario)

# Función que elimina el usuario
def eliminar_usuario():
    seleccion = listbox_usuarios.curselection()
    # Controlar que deba haber un usuario seleccionado
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar.")
        return
    listbox_usuarios.delete(seleccion)

# Crear ventana principal
root = tk.Tk()
root.title("Registro de Usuarios")
root.geometry("400x500")

# Crear la entrada para el nombre
tk.Label(root, text="Nombre:").pack()
entrada_nombre = tk.Entry(root)
entrada_nombre.pack(pady=5)

# Crear etiqueta para la scale de edad
etiqueta_nombre = tk.Label(root, text="Edad:")
etiqueta_nombre.pack(pady=5)

# Crear scale para la edad
escala_edad = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
escala_edad.pack(pady=5)

# Creo variable de control para los radiobuttons y dejo un valor por defecto
var_radiobutton = tk.StringVar()
var_radiobutton.set("female")

# Crear radiobuttons
radiobutton1 = tk.Radiobutton(root, text="Masculino",
                              variable=var_radiobutton,
                              value="male")
radiobutton1.pack(pady=5)
radiobutton2 = tk.Radiobutton(root, text="Femenino",
                              variable=var_radiobutton,
                              value="female")
radiobutton2.pack(pady=5)
radiobutton3 = tk.Radiobutton(root,text="Otro",
                              variable=var_radiobutton,
                              value="other")
radiobutton3.pack(pady=5)

# Crear todos los botones
boton_add = tk.Button(root, text="Añadir", command=añadir_usuario)
boton_add.pack(pady=5)

boton_eliminar = tk.Button(root, text="Eliminar", command=eliminar_usuario)
boton_eliminar.pack(pady=5)

boton_salir = tk.Button(root, text="Salir", command=salir_app)
boton_salir.pack(pady=5)

# Creo un frame para meter el listbox con scrollbar
frame_lista = tk.Frame(root)
frame_lista.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar_vert = tk.Scrollbar(frame_lista)
scrollbar_vert.pack(side=tk.RIGHT, fill=tk.Y)

listbox_usuarios = tk.Listbox(frame_lista, yscrollcommand=scrollbar_vert.set, width=50, height=10)
listbox_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_vert.config(command=listbox_usuarios.yview)

# Creo el menú
menu_principal = tk.Menu(root)
root.config(menu=menu_principal)

menu_lista = tk.Menu(menu_principal, tearoff=0)
menu_lista.add_command(label="Guardar Lista", command=guardar_lista)
menu_lista.add_command(label="Cargar Lista", command=cargar_lista)

menu_principal.add_cascade(label="Lista", menu=menu_lista)

root.mainloop()