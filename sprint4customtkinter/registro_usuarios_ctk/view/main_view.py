import customtkinter as ctk
from PIL import Image

class MainView(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True)

        # Empiezo configurando la ventana principal para poder hacer que la aplicación se adapte al tamaño que
        # elija el usuario (responsive)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

        # Creo un frame superior donde va a estar el menú principal, los filtros y los botones de eliminar y añadir
        self.frame_superior = ctk.CTkFrame(self)
        self.frame_superior.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.frame_superior.columnconfigure(2, weight=1)  # Entry ocupa espacio central

        # Menú desplegable

        # Creo menú archivo con la opción que nos da CTk
        self.menu_archivo = ctk.CTkOptionMenu(
            self.frame_superior,
            values=["Guardar", "Cargar", "Salir"],
            command=self.opcion_archivo_seleccionada,
            width=80
        )
        self.menu_archivo.set("Archivo")
        self.menu_archivo.grid(row=0, column=0, padx=(10, 5))

        # Menú ayuda
        self.menu_ayuda = ctk.CTkOptionMenu(
            self.frame_superior,
            values=["Acerca de"],
            command=self.opcion_ayuda_seleccionada,
            width=80
        )
        self.menu_ayuda.set("Ayuda")
        self.menu_ayuda.grid(row=0, column=1, padx=(0, 10))

        # Label + entry para buscar por nombre
        self.label_buscar = ctk.CTkLabel(self.frame_superior, text="Buscar:")
        self.label_buscar.grid(row=0, column=2, padx=(10,5), pady=5)

        self.entry_buscar = ctk.CTkEntry(self.frame_superior, placeholder_text="Introduce un nombre")
        self.entry_buscar.grid(row=0, column=3, padx=(0,10), pady=5, sticky="ew")

        # Label + option menu para filtrar por género
        self.label_genero = ctk.CTkLabel(self.frame_superior, text="Género:")
        self.label_genero.grid(row=0, column=4, padx=5)

        self.option_genero = ctk.CTkOptionMenu(self.frame_superior, values=["otro", "masculino", "femenino"])
        self.option_genero.grid(row=0, column=5, padx=5)

        # Botones de añadir, eliminar, editar y salir
        self.boton_eliminar = ctk.CTkButton(self.frame_superior, text="Eliminar", width=80,
                                            command=self.controller.eliminar_usuario)
        self.boton_eliminar.grid(row=0, column=6, padx=5)

        self.boton_añadir = ctk.CTkButton(self.frame_superior, text="Añadir", width=80,
                                          command=self.controller.abrir_formulario)
        self.boton_añadir.grid(row=0, column=7, padx=5)

        self.boton_editar = ctk.CTkButton(self.frame_superior, text="Editar", width=80,
                                          command=self.controller.editar_usuario)
        self.boton_editar.grid(row=0, column=8, padx=5)

        self.boton_salir = ctk.CTkButton(self.frame_superior, text="Salir", width=80,
                                         fg_color="gray30", command=self.controller.salir_app)
        self.boton_salir.grid(row=0, column=9, padx=5)

        # Panel izquierdo (ScrollableFrame)
        self.frame_lista = ctk.CTkFrame(self)
        self.frame_lista.grid(row=1, column=0, sticky="nsew", padx=(10,5), pady=(0,10))
        self.frame_lista.rowconfigure(0, weight=1)
        self.frame_lista.columnconfigure(0, weight=1)

        # Creo el ScrollableFrame
        self.scrollable_lista = ctk.CTkScrollableFrame(self.frame_lista, label_text="Usuarios registrados")
        self.scrollable_lista.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Panel derecho (detalle y preview)
        self.frame_preview = ctk.CTkFrame(self)
        self.frame_preview.grid(row=1, column=1, sticky="nsew", padx=(5,10), pady=(0,10))
        self.frame_preview.columnconfigure(0, weight=1)

        # Creo un label para mostrar la imagen de avatar
        self.label_avatar = ctk.CTkLabel(self.frame_preview, text="(sin foto)", height=150, fg_color="gray30",
                                         corner_radius=10)
        self.label_avatar.pack(padx=10, pady=(20,10), fill="both")

        # Creo un label para mostrar el nombre
        self.label_nombre = ctk.CTkLabel(self.frame_preview, text="Nombre: -", anchor="w")
        self.label_nombre.pack(fill="x", padx=20, pady=5)

        # Creo un label para mostrar la edad
        self.label_edad = ctk.CTkLabel(self.frame_preview, text="Edad: -", anchor="w")
        self.label_edad.pack(fill="x", padx=20, pady=5)

        # Creo un label para mostrar el género
        self.label_genero = ctk.CTkLabel(self.frame_preview, text="Género: -", anchor="w")
        self.label_genero.pack(fill="x", padx=20, pady=5)

    # Funciones

    # Función asociada al menú Archivo > Salir que cierra la app
    def opcion_archivo_seleccionada(self, opcion):
        if opcion == "Salir":
            self.controller.salir_app()
        elif opcion == "Guardar":
            self.controller.guardar_usuarios()
        elif opcion == "Cargar":
            self.controller.cargar_usuarios()

    # Función asociada al menú Ayuda que mostrará un mensaje
    def opcion_ayuda_seleccionada(self, opcion):
        if opcion == "Acerca de":
            self.controller.mostrar_ayuda()

    # Función que rellena el ScrollableFrame con la información de los usuarios y que borra el contenido
    # cada vez que se usa
    def mostrar_usuarios(self, lista_usuarios):
        # Borrar contenido antiguo
        for widget in self.scrollable_lista.winfo_children():
            widget.destroy()

        # Mostrar un mensaje cuando no hay usuarios en la lista
        if not lista_usuarios:
            label_vacio = ctk.CTkLabel(self.scrollable_lista, text="(Sin usuarios)")
            label_vacio.pack(pady=10)
            return

        # Crea botones con el nombre de cada usuario, los cuales se van a poder pulsar y mostrarán
        # la información asociada a cada uno
        for usuario in lista_usuarios:
            boton = ctk.CTkButton(
                self.scrollable_lista,
                text=usuario.nombre,
                command=lambda u=usuario: self.controller.seleccionar_usuario(u),
                anchor="w"
            )
            boton.pack(fill="x", padx=5, pady=2)


    # Rellena la lista con la información de cada usuario
    def mostrar_detalle_usuario(self, usuario):
        # Intentar cargar el avatar usando PIL
        try:
            if usuario.avatar:  # si hay ruta definida
                imagen = ctk.CTkImage(Image.open(usuario.avatar), size=(150, 150))
                self.label_avatar.configure(image=imagen, text="")
                self.label_avatar.image = imagen  # necesario para que no lo borre el garbage collector
            else:
                raise FileNotFoundError
        except Exception:
            # Si falla, mostrar texto por defecto
            self.label_avatar.configure(image=None, text="(sin foto)")

        # Actualizar datos de usuario
        self.label_nombre.configure(text=f"Nombre: {usuario.nombre}")
        self.label_edad.configure(text=f"Edad: {usuario.edad}")
        self.label_genero_preview.configure(text=f"Género: {usuario.genero}")



