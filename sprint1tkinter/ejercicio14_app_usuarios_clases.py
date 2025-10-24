import tkinter as tk
from tkinter import messagebox

class RegistroApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Ejercicio 14: Registro de usuarios (Clases)")

        # Crear la entrada para el nombre
        self.etiqueta_nombre = tk.Label(root, text="Nombre:")
        self.etiqueta_nombre.pack()

        self.entrada_nombre = tk.Entry(root)
        self.entrada_nombre.pack(pady=5)

        # Crear etiqueta para la scale de edad
        self.etiqueta_edad = tk.Label(root, text="Edad:")
        self.etiqueta_edad.pack(pady=5)

        # Crear scale para la edad
        self.escala_edad = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
        self.escala_edad.pack(pady=5)

        # Creo variable de control para los radiobuttons y dejo un valor por defecto
        self.var_radiobutton = tk.StringVar()
        self.var_radiobutton.set("female")

        # Crear radiobuttons
        self.radiobutton1 = tk.Radiobutton(root, text="Masculino",
                                      variable=self.var_radiobutton,
                                      value="male")
        self.radiobutton1.pack(pady=5)
        self.radiobutton2 = tk.Radiobutton(root, text="Femenino",
                                      variable=self.var_radiobutton,
                                      value="female")
        self.radiobutton2.pack(pady=5)
        self.radiobutton3 = tk.Radiobutton(root, text="Otro",
                                      variable=self.var_radiobutton,
                                      value="other")
        self.radiobutton3.pack(pady=5)

        # Crear todos los botones
        self.boton_add = tk.Button(root, text="Añadir", command=self.añadir_usuario)
        self.boton_add.pack(pady=5)

        self.boton_eliminar = tk.Button(root, text="Eliminar", command=self.eliminar_usuario)
        self.boton_eliminar.pack(pady=5)

        self.boton_salir = tk.Button(root, text="Salir", command=self.salir_app)
        self.boton_salir.pack(pady=5)

        # Creo un frame para meter el listbox con scrollbar
        self.frame_lista = tk.Frame(root)
        self.frame_lista.pack(pady=10, fill=tk.BOTH, expand=True)

        self.scrollbar_vert = tk.Scrollbar(self.frame_lista)
        self.scrollbar_vert.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_usuarios = tk.Listbox(self.frame_lista, yscrollcommand=self.scrollbar_vert.set, width=50, height=10)
        self.listbox_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_vert.config(command=self.listbox_usuarios.yview)

        # Creo el menú
        self.menu_principal = tk.Menu(root)
        self.root.config(menu=self.menu_principal)

        self.menu_lista = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_lista.add_command(label="Guardar Lista", command=self.guardar_lista)
        self.menu_lista.add_command(label="Cargar Lista", command=self.cargar_lista)

        self.menu_principal.add_cascade(label="Lista", menu=self.menu_lista)

    # Función asociada al menú que muestra el mensaje de "Guardar lista"
    def guardar_lista(self):
        messagebox.showinfo("Guardar Lista", "Lista guardada")

    # Función asociada al menú que muestra el mensaje de "Cargar lista"
    def cargar_lista(self):
        messagebox.showinfo("Cargar Lista", "Lista cargada")

    # Función asociada al botón de salir de la app
    def salir_app(self):
        self.root.quit()

    # Función para añadir un usuario a la lista
    def añadir_usuario(self):
        nombre = self.entrada_nombre.get().strip()
        edad = self.escala_edad.get()
        genero = self.var_radiobutton.get()

        # Comprobar que el campo "Nombre" no queda vacío
        if not nombre:
            messagebox.showwarning("Advertencia", "Debe ingresar un nombre.")
            return

        # Crear la cadena que se muestra en el listbox y añadirla
        usuario = f"{nombre} - {edad} años - {genero}"
        self.listbox_usuarios.insert(tk.END, usuario)

    # Función que elimina el usuario
    def eliminar_usuario(self):
        seleccion = self.listbox_usuarios.curselection()
        # Controlar que deba haber un usuario seleccionado
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar.")
            return
        self.listbox_usuarios.delete(seleccion)

# Crear instancia
root = tk.Tk()
app = RegistroApp(root)
root.mainloop()




