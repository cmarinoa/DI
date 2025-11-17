import customtkinter as ctk
from view.main_view import MainView
from model.usuario_model import GestorUsuarios, Usuario
import tkinter.messagebox as messagebox
from PIL import Image
import os
import threading
import time


class AppController:
    def __init__(self, app):
        self.app = app
        self.modelo = GestorUsuarios()
        self.usuarios_filtrados = []  # Lista para usuarios filtrados

        # Variables para auto-guardado
        self.auto_guardar_activo = False
        self.hilo_auto_guardar = None
        self.detener_hilo = False

        # Cargar usuarios al iniciar la app
        try:
            self.modelo.cargar_csv()
            self.usuarios_filtrados = self.modelo.listar()
        except FileNotFoundError:
            # Si el archivo no existe, empezar con lista vacía
            self.usuarios_filtrados = []
        except Exception as e:
            messagebox.showwarning("Advertencia", f"No se pudieron cargar los usuarios: {str(e)}")
            self.usuarios_filtrados = []

        # Vista principal
        self.vista = MainView(self.app, controller=self)

        # Recoge los datos del modelo y los vuelca en la interfaz
        self.actualizar_vista()

        # Asegurarse de que el hilo se detenga al cerrar la aplicación
        self.app.protocol("WM_DELETE_WINDOW", self.salir_app)

    # Mostrar detalles del usuario
    def seleccionar_usuario(self, usuario):
        self.vista.mostrar_detalle_usuario(usuario)

    # Función asociada al menú desplegable "Ayuda"
    def mostrar_ayuda(self):
        messagebox.showinfo(
            title="Ayuda",
            message="Contacte con nuestro equipo de soporte:\nsoportesuperguay@soportegenial.com"
        )

    # Función que elimina el usuario
    def eliminar_usuario(self):
        # Obtener el índice del usuario seleccionado en la lista filtrada
        indice_filtrado = self.vista.obtener_indice_seleccionado()

        if indice_filtrado is None:
            messagebox.showwarning("Advertencia", "Selecciona un usuario de la lista para eliminar")
            return

        # Obtener el usuario de la lista filtrada
        usuario_filtrado = self.usuarios_filtrados[indice_filtrado]

        # Confirmar eliminación con el usuario
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que quieres eliminar a {usuario_filtrado.nombre}?"
        )

        if not confirmar:
            return

        try:
            # Encontrar el índice real en la lista completa buscando por nombre y otros datos
            indice_real = None
            for i, usuario in enumerate(self.modelo.listar()):
                if (usuario.nombre == usuario_filtrado.nombre and
                        usuario.edad == usuario_filtrado.edad and
                        usuario.genero == usuario_filtrado.genero):
                    indice_real = i
                    break

            if indice_real is not None:
                # Eliminar el usuario usando la función del modelo
                self.modelo.eliminar(indice_real)

                # Actualizar la vista con la lista actualizada
                self.aplicar_filtros()

                # Limpiar el panel de detalles
                self.vista.mostrar_detalle_usuario(None)

                # Guardar los cambios en el CSV
                try:
                    self.modelo.guardar_csv()
                    self.vista.actualizar_estado("Usuario eliminado correctamente.",
                                                 len(self.modelo.listar()),
                                                 len(self.usuarios_filtrados))
                except Exception as e:
                    self.vista.actualizar_estado(f"Usuario eliminado pero error guardando: {str(e)}",
                                                 len(self.modelo.listar()),
                                                 len(self.usuarios_filtrados))
            else:
                messagebox.showerror("Error", "No se pudo encontrar el usuario para eliminar")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el usuario: {str(e)}")

    # Función para editar el usuario desde doble clic
    def editar_usuario_doble_clic(self, usuario_filtrado, indice_filtrado):
        # Encontrar el usuario real en la lista completa
        usuario_real = None
        for usuario in self.modelo.listar():
            if (usuario.nombre == usuario_filtrado.nombre and
                    usuario.edad == usuario_filtrado.edad and
                    usuario.genero == usuario_filtrado.genero):
                usuario_real = usuario
                break

        if usuario_real:
            self.abrir_formulario(usuario_real, indice_filtrado)
        else:
            messagebox.showerror("Error", "No se pudo encontrar el usuario para editar")

    # Función para buscar usuarios en tiempo real
    def buscar_usuarios(self, *args):
        self.aplicar_filtros()

    # Función para filtrar por género
    def filtrar_por_genero(self, genero):
        self.aplicar_filtros()

    # Función que aplica todos los filtros
    def aplicar_filtros(self):
        texto_busqueda = self.vista.obtener_texto_busqueda()
        genero_seleccionado = self.vista.obtener_genero_seleccionado()

        todos_usuarios = self.modelo.listar()
        self.usuarios_filtrados = []

        for usuario in todos_usuarios:
            # Filtro por texto - buscar en el nombre (case insensitive)
            coincide_texto = texto_busqueda == "" or texto_busqueda in usuario.nombre.lower()

            # Filtro por género
            coincide_genero = genero_seleccionado == "todos" or usuario.genero == genero_seleccionado

            if coincide_texto and coincide_genero:
                self.usuarios_filtrados.append(usuario)

        self.actualizar_vista()

    # Función para actualizar la vista
    def actualizar_vista(self):
        self.vista.mostrar_usuarios(self.usuarios_filtrados)
        self.vista.actualizar_estado("Listo.",
                                     len(self.modelo.listar()),
                                     len(self.usuarios_filtrados))

    # Función que abre una ventana para añadir un usuario
    def abrir_formulario(self, usuario_editar=None, indice_editar=None):
        # Crear formulario modal con CTkToplevel
        formulario = ctk.CTkToplevel(self.app)

        if usuario_editar:
            formulario.title("Editar Usuario")
            es_edicion = True
        else:
            formulario.title("Añadir Usuario")
            es_edicion = False

        formulario.geometry("400x600")
        formulario.resizable(False, False)
        # Modal respecto al padre
        formulario.transient(self.app)
        # Impide interactuar con la ventana principal
        formulario.grab_set()

        # Centrar la ventana
        self.centrar_ventana(formulario, 400, 600)

        # Variables para los datos del formulario
        nombre_var = ctk.StringVar()
        edad_var = ctk.IntVar(value=18)
        genero_var = ctk.StringVar(value="otro")
        avatar_var = ctk.StringVar()

        # Si estamos editando, cargar datos del usuario
        if es_edicion and usuario_editar:
            nombre_var.set(usuario_editar.nombre)
            edad_var.set(usuario_editar.edad)
            genero_var.set(usuario_editar.genero)
            avatar_var.set(usuario_editar.avatar)

        # Título
        titulo = ctk.CTkLabel(formulario, text="Añadir Usuario" if not es_edicion else "Editar Usuario",
                              font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        # Frame principal
        frame_principal = ctk.CTkFrame(formulario)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=10)

        # Configurar grid para que el frame se expanda
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.rowconfigure(8, weight=1)

        # Label + entry para el nombre
        label_nombre = ctk.CTkLabel(frame_principal, text="Nombre:")
        label_nombre.grid(row=0, column=0, sticky="w", pady=(0, 5))

        entry_nombre = ctk.CTkEntry(frame_principal, textvariable=nombre_var, placeholder_text="Introduce el nombre")
        entry_nombre.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Label para la escala
        label_edad = ctk.CTkLabel(frame_principal, text="Edad (0-100):")
        label_edad.grid(row=2, column=0, sticky="w", pady=(0, 5))

        # Función para actualizar el label de edad
        def actualizar_edad(val):
            label_edad_valor.configure(text=f"Edad: {int(float(val))}")

        # Scale para edad
        scale_edad = ctk.CTkSlider(frame_principal, from_=0, to=100, number_of_steps=100,
                                   variable=edad_var, command=actualizar_edad)
        scale_edad.grid(row=3, column=0, sticky="ew", pady=(0, 5))

        # Label que muestra la edad actual
        label_edad_valor = ctk.CTkLabel(frame_principal, text=f"Edad: {edad_var.get()}")
        label_edad_valor.grid(row=4, column=0, sticky="w", pady=(0, 10))

        # Label para el género
        label_genero = ctk.CTkLabel(frame_principal, text="Género:")
        label_genero.grid(row=5, column=0, sticky="w", pady=(0, 5))

        # Frame para radio buttons de género
        frame_genero = ctk.CTkFrame(frame_principal)
        frame_genero.grid(row=6, column=0, sticky="ew", pady=(0, 10))

        # Radio buttons para género
        radio_masculino = ctk.CTkRadioButton(frame_genero, text="Masculino", variable=genero_var, value="masculino")
        radio_masculino.pack(anchor="w", pady=2)

        radio_femenino = ctk.CTkRadioButton(frame_genero, text="Femenino", variable=genero_var, value="femenino")
        radio_femenino.pack(anchor="w", pady=2)

        radio_otro = ctk.CTkRadioButton(frame_genero, text="Otro", variable=genero_var, value="otro")
        radio_otro.pack(anchor="w", pady=2)

        # Label para los avatares
        label_avatar = ctk.CTkLabel(frame_principal, text="Avatar:")
        label_avatar.grid(row=7, column=0, sticky="w", pady=(0, 5))

        # Frame para los botones de avatar
        frame_avatars = ctk.CTkFrame(frame_principal)
        frame_avatars.grid(row=8, column=0, sticky="ew", pady=(0, 10))

        # Preview del avatar - DEFINIR PRIMERO para que esté disponible en el scope
        label_preview = ctk.CTkLabel(frame_principal, text="Selecciona un avatar", height=120, fg_color="gray30",
                                     corner_radius=10)
        label_preview.grid(row=9, column=0, sticky="ew", pady=(0, 10))

        # Función para seleccionar avatar - AHORA SÍ PUEDE ACCEDER A label_preview
        def seleccionar_avatar(avatar_file):
            avatar_var.set(avatar_file)

            # Intentar cargar y mostrar la imagen
            try:
                avatar_path = os.path.join("assets", avatar_file)
                if os.path.exists(avatar_path):
                    image = Image.open(avatar_path)
                    image = image.resize((100, 100), Image.Resampling.LANCZOS)
                    imagen_avatar = ctk.CTkImage(image, size=(100, 100))
                    label_preview.configure(image=imagen_avatar, text="")
                    label_preview.image = imagen_avatar  # Mantener referencia
                else:
                    label_preview.configure(image=None, text="Avatar no encontrado")
            except Exception as e:
                print(f"Error cargando avatar: {e}")
                label_preview.configure(image=None, text="Error cargando avatar")

        # Botones para seleccionar avatar
        avatares = [("avatar1.png", "Avatar 1"), ("avatar2.png", "Avatar 2"), ("avatar3.png", "Avatar 3")]

        for i, (avatar_file, texto) in enumerate(avatares):
            btn = ctk.CTkButton(
                frame_avatars,
                text=texto,
                command=lambda av=avatar_file: seleccionar_avatar(av),
                width=90
            )
            btn.grid(row=0, column=i, padx=5, pady=5)

        # Si estamos editando, seleccionar el avatar actual
        if es_edicion and usuario_editar and usuario_editar.avatar:
            seleccionar_avatar(usuario_editar.avatar)

        # Botones confirmar y cancelar del formulario
        # Frame para botones
        frame_botones = ctk.CTkFrame(frame_principal)
        frame_botones.grid(row=10, column=0, sticky="ew", pady=(10, 0))

        # Función para guardar usuario
        def guardar_usuario():
            nombre = nombre_var.get().strip()
            edad = edad_var.get()
            genero = genero_var.get()
            avatar = avatar_var.get()

            # Controlar que toda la información sea añadida
            if not nombre:
                mostrar_error("El nombre no puede estar vacío")
                return

            if not avatar:
                mostrar_error("Selecciona un avatar")
                return

            # Guardar en el modelo
            try:
                nuevo_usuario = Usuario(nombre, edad, genero, avatar)

                if es_edicion:
                    # Encontrar el índice real en la lista completa
                    indice_real = None
                    for i, u in enumerate(self.modelo.listar()):
                        if u.nombre == usuario_editar.nombre and u.edad == usuario_editar.edad:
                            indice_real = i
                            break

                    if indice_real is not None:
                        self.modelo.actualizar(indice_real, nuevo_usuario)
                        mensaje = "Usuario actualizado correctamente"
                    else:
                        raise Exception("No se pudo encontrar el usuario a editar")
                else:
                    self.modelo.añadir(nuevo_usuario)
                    mensaje = "Usuario añadido correctamente"

                self.aplicar_filtros()
                self.vista.actualizar_estado(mensaje,
                                             len(self.modelo.listar()),
                                             len(self.usuarios_filtrados))
                formulario.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el usuario: {str(e)}")

        # Función para mostrar errores temporales
        def mostrar_error(mensaje):
            error_label = ctk.CTkLabel(formulario, text=mensaje, text_color="red")
            error_label.pack()
            formulario.after(3000, error_label.destroy)

        # Botón confirmar en el formulario
        boton_confirmar = ctk.CTkButton(
            frame_botones,
            text="Confirmar",
            command=guardar_usuario,
            fg_color="#2AA876",
            hover_color="#228B69",
            width=120
        )
        boton_confirmar.pack(side="right", padx=5)

        # Botón cancelar en el formulario
        boton_cancelar = ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            command=formulario.destroy,
            fg_color="gray30",
            width=120
        )
        boton_cancelar.pack(side="right", padx=5)

    # Función para centrar ventanas
    def centrar_ventana(self, ventana, ancho, alto):
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

    def guardar_usuarios(self):
        try:
            self.modelo.guardar_csv()
            self.vista.actualizar_estado("Usuarios guardados correctamente.",
                                         len(self.modelo.listar()),
                                         len(self.usuarios_filtrados))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los usuarios: {str(e)}")

    def cargar_usuarios(self):
        try:
            self.modelo.cargar_csv()
            self.aplicar_filtros()
            self.vista.actualizar_estado("Usuarios cargados correctamente.",
                                         len(self.modelo.listar()),
                                         len(self.usuarios_filtrados))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los usuarios: {str(e)}")

    # Creo funciones para controlar el autoguardado no bloqueante con hilos

    def toggle_auto_guardar(self):
        #Activa o desactiva el auto-guardado
        if self.auto_guardar_activo:
            self.detener_auto_guardar()
        else:
            self.iniciar_auto_guardar()

    def iniciar_auto_guardar(self):
        #Inicia el hilo de auto-guardado
        if self.auto_guardar_activo:
            return

        self.auto_guardar_activo = True
        self.detener_hilo = False

        # Actualizar UI
        self.vista.actualizar_auto_guardar_ui(True, "Auto-guardado activado (cada 10s)")

        # Crear y iniciar hilo
        self.hilo_auto_guardar = threading.Thread(target=self._hilo_auto_guardar, daemon=True)
        self.hilo_auto_guardar.start()

    def detener_auto_guardar(self):
        #Detiene el hilo de auto-guardado
        if not self.auto_guardar_activo:
            return

        self.detener_hilo = True
        self.auto_guardar_activo = False

        # Actualizar UI
        self.vista.actualizar_auto_guardar_ui(False, "Auto-guardado desactivado")

    def _hilo_auto_guardar(self):
        #Hilo que ejecuta el auto-guardado cada 10 segundos
        intervalo = 10  # segundos

        while not self.detener_hilo:
            # Esperar el intervalo
            for i in range(intervalo * 10):  # Dividir en intervalos de 0.1s para respuesta rápida
                if self.detener_hilo:
                    return
                time.sleep(0.1)

            if self.detener_hilo:
                return

            # Ejecutar auto-guardado
            try:
                self.modelo.guardar_csv()
                # Usar after para actualizar la UI desde el hilo principal
                self.app.after(0, self._mostrar_auto_guardado_exitoso)
            except Exception as e:
                # Usar after para mostrar error desde el hilo principal
                self.app.after(0, lambda: self._mostrar_error_auto_guardado(str(e)))

    def _mostrar_auto_guardado_exitoso(self):
        """Muestra mensaje de auto-guardado exitoso (ejecutado en hilo principal)"""
        if self.auto_guardar_activo:
            self.vista.actualizar_estado("Auto-guardado exitoso.",
                                         len(self.modelo.listar()),
                                         len(self.usuarios_filtrados))

    def _mostrar_error_auto_guardado(self, error):
        """Muestra error de auto-guardado (ejecutado en hilo principal)"""
        if self.auto_guardar_activo:
            self.vista.actualizar_estado(f"Error en auto-guardado: {error}",
                                         len(self.modelo.listar()),
                                         len(self.usuarios_filtrados))

    # Función para salir de la app
    def salir_app(self):
        # Detener el hilo de auto-guardado antes de salir
        self.detener_auto_guardar()

        # Esperar un poco a que el hilo se detenga (máximo 1 segundo)
        if self.hilo_auto_guardar and self.hilo_auto_guardar.is_alive():
            self.hilo_auto_guardar.join(timeout=1.0)

        self.app.destroy()