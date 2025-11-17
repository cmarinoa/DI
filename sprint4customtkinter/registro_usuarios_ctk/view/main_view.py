import customtkinter as ctk
from PIL import Image
import os


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
        self.label_buscar.grid(row=0, column=2, padx=(10, 5), pady=5)

        self.entry_buscar = ctk.CTkEntry(self.frame_superior, placeholder_text="Introduce un nombre")
        self.entry_buscar.grid(row=0, column=3, padx=(0, 10), pady=5, sticky="ew")

        # Trace para búsqueda en tiempo real con trace_add
        self.texto_busqueda = ctk.StringVar()
        self.entry_buscar.configure(textvariable=self.texto_busqueda)
        self.texto_busqueda.trace_add("write", self.controller.buscar_usuarios)

        # Label + option menu para filtrar por género
        self.label_genero = ctk.CTkLabel(self.frame_superior, text="Género:")
        self.label_genero.grid(row=0, column=4, padx=5)

        self.option_genero = ctk.CTkOptionMenu(
            self.frame_superior,
            values=["todos", "masculino", "femenino", "otro"],
            command=self.controller.filtrar_por_genero
        )
        self.option_genero.set("todos")
        self.option_genero.grid(row=0, column=5, padx=5)

        # Botones de añadir y eliminar (quitamos editar y salir)
        self.boton_eliminar = ctk.CTkButton(self.frame_superior, text="Eliminar", width=80,
                                            command=self.controller.eliminar_usuario)
        self.boton_eliminar.grid(row=0, column=6, padx=5)

        self.boton_añadir = ctk.CTkButton(self.frame_superior, text="Añadir", width=80,
                                          command=self.controller.abrir_formulario)
        self.boton_añadir.grid(row=0, column=7, padx=5)

        # Botón de auto-guardado
        self.boton_auto_guardar = ctk.CTkButton(
            self.frame_superior,
            text="Auto-guardar: OFF",
            width=100,
            command=self.controller.toggle_auto_guardar,
            fg_color="gray30",
            hover_color="gray40"
        )
        self.boton_auto_guardar.grid(row=0, column=8, padx=5)

        # Panel izquierdo (ScrollableFrame)
        self.frame_lista = ctk.CTkFrame(self)
        self.frame_lista.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))
        self.frame_lista.rowconfigure(0, weight=1)
        self.frame_lista.columnconfigure(0, weight=1)

        # Creo el ScrollableFrame
        self.scrollable_lista = ctk.CTkScrollableFrame(self.frame_lista, label_text="Usuarios registrados")
        self.scrollable_lista.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Panel derecho (detalle y preview)
        self.frame_preview = ctk.CTkFrame(self)
        self.frame_preview.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        self.frame_preview.columnconfigure(0, weight=1)

        # Creo un label para mostrar la imagen de avatar
        self.label_avatar = ctk.CTkLabel(self.frame_preview, text="sin foto", height=150, fg_color="transparent",
                                         corner_radius=10)
        self.label_avatar.pack(padx=10, pady=(20, 10), fill="both")

        # Creo un label para mostrar el nombre
        self.label_nombre = ctk.CTkLabel(self.frame_preview, text="Nombre: -", anchor="w")
        self.label_nombre.pack(fill="x", padx=20, pady=5)

        # Creo un label para mostrar la edad
        self.label_edad = ctk.CTkLabel(self.frame_preview, text="Edad: -", anchor="w")
        self.label_edad.pack(fill="x", padx=20, pady=5)

        # Creo un label para mostrar el género
        self.label_genero_preview = ctk.CTkLabel(self.frame_preview, text="Género: -", anchor="w")
        self.label_genero_preview.pack(fill="x", padx=20, pady=5)

        # Barra de estado
        self.frame_estado = ctk.CTkFrame(self)
        self.frame_estado.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        self.frame_estado.columnconfigure(0, weight=1)

        self.label_estado = ctk.CTkLabel(self.frame_estado, text="Listo. 0 usuarios visibles.")
        self.label_estado.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.label_auto_guardar = ctk.CTkLabel(self.frame_estado, text="Auto-guardar (10s): OFF")
        self.label_auto_guardar.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        # Variable para guardar el usuario seleccionado
        self.usuario_seleccionado = None
        self.indice_seleccionado = None

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

        # Resetear selección
        self.usuario_seleccionado = None
        self.indice_seleccionado = None

        # Mostrar un mensaje cuando no hay usuarios en la lista
        if not lista_usuarios:
            label_vacio = ctk.CTkLabel(self.scrollable_lista, text="(Sin usuarios)")
            label_vacio.pack(pady=10)
            return

        # Crea botones con el nombre de cada usuario, los cuales se van a poder pulsar y mostrarán
        # la información asociada a cada uno o editar si haces doble click
        for indice, usuario in enumerate(lista_usuarios):
            # Frame para cada usuario en la lista
            frame_usuario = ctk.CTkFrame(self.scrollable_lista)
            frame_usuario.pack(fill="x", padx=5, pady=2)

            # Botón con nombre del usuario
            boton = ctk.CTkButton(
                frame_usuario,
                text=f"{usuario.nombre} — {usuario.edad} — {usuario.genero}",
                command=lambda u=usuario, idx=indice: self.seleccionar_usuario(u, idx),
                anchor="w",
                fg_color="transparent",
                hover_color="gray25",
                text_color=("gray10", "gray90")
            )
            boton.pack(fill="x")

            # Bind doble clic para editar
            boton.bind("<Double-Button-1>",
                       lambda e, u=usuario, idx=indice: self.controller.editar_usuario_doble_clic(u, idx))

    # Función para seleccionar usuario de la lista
    def seleccionar_usuario(self, usuario, indice):
        self.usuario_seleccionado = usuario
        self.indice_seleccionado = indice
        self.controller.seleccionar_usuario(usuario)

    # Función para obtener el usuario seleccionado
    def obtener_usuario_seleccionado(self):
        return self.usuario_seleccionado

    # Función para obtener el índice seleccionado
    def obtener_indice_seleccionado(self):
        return self.indice_seleccionado

    # Rellena la lista con la información de cada usuario
    def mostrar_detalle_usuario(self, usuario):
        # Intentar cargar el avatar usando PIL
        try:
            if usuario:  # si hay usuario seleccionado
                if usuario.avatar:  # si hay ruta definida
                    avatar_path = os.path.join("assets", usuario.avatar)
                    imagen = ctk.CTkImage(Image.open(avatar_path), size=(150, 150))
                    self.label_avatar.configure(image=imagen, text="")
                    self.label_avatar.image = imagen  # necesario para que no lo borre el garbage collector
                else:
                    raise FileNotFoundError
            else:
                raise FileNotFoundError
        except Exception:
            # Si falla, mostrar texto por defecto
            self.label_avatar.configure(image=None, text="(sin foto)")

        # Actualizar datos de usuario
        if usuario:
            self.label_nombre.configure(text=f"Nombre: {usuario.nombre}")
            self.label_edad.configure(text=f"Edad: {usuario.edad}")
            self.label_genero_preview.configure(text=f"Género: {usuario.genero}")
        else:
            # Si no hay usuario, mostrar valores por defecto
            self.label_nombre.configure(text="Nombre: -")
            self.label_edad.configure(text="Edad: -")
            self.label_genero_preview.configure(text="Género: -")

    # Función para actualizar la barra de estado
    def actualizar_estado(self, mensaje, total_usuarios, usuarios_visibles):
        texto_estado = f"{mensaje} {usuarios_visibles} usuarios visibles."
        self.label_estado.configure(text=texto_estado)

    # Función para obtener el texto de búsqueda
    def obtener_texto_busqueda(self):
        return self.texto_busqueda.get().strip().lower()

    # Función para obtener el género seleccionado
    def obtener_genero_seleccionado(self):
        return self.option_genero.get()

    # Función para limpiar filtros
    def limpiar_filtros(self):
        self.texto_busqueda.set("")
        self.option_genero.set("todos")

    # Función para actualizar el estado del auto-guardado
    def actualizar_auto_guardar_ui(self, activado, mensaje=None):
        if activado:
            self.boton_auto_guardar.configure(text="Auto-guardar: ON", fg_color="#2AA876", hover_color="#228B69")
            self.label_auto_guardar.configure(text="Auto-guardar (10s): ON")
        else:
            self.boton_auto_guardar.configure(text="Auto-guardar: OFF", fg_color="gray30", hover_color="gray40")
            self.label_auto_guardar.configure(text="Auto-guardar (10s): OFF")

        if mensaje:
            self.label_estado.configure(text=mensaje)