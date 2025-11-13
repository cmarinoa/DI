import customtkinter as ctk
from view.main_view import MainView
from model.usuario_model import GestorUsuarios, Usuario
import tkinter.messagebox as messagebox
from PIL import Image
import os

import customtkinter as ctk
from view.main_view import MainView
from model.usuario_model import GestorUsuarios, Usuario
import tkinter.messagebox as messagebox
from PIL import Image
import os


class AppController:
    def __init__(self, app):
        self.app = app
        self.modelo = GestorUsuarios()

        # Cargar usuarios al iniciar la app
        try:
            self.modelo.cargar_csv()
        except FileNotFoundError:
            # Si el archivo no existe, empezar con lista vacía
            pass
        except Exception as e:
            messagebox.showwarning("Advertencia", f"No se pudieron cargar los usuarios: {str(e)}")

        # Vista principal
        self.vista = MainView(self.app, controller=self)

        # Recoge los datos del modelo y los vuelca en la interfaz
        self.vista.mostrar_usuarios(self.modelo.listar())

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
        # Obtener el índice del usuario seleccionado
        indice = self.vista.obtener_indice_seleccionado()

        if indice is None:
            import tkinter.messagebox as messagebox
            messagebox.showwarning("Advertencia", "Selecciona un usuario de la lista para eliminar")
            return

        # Obtener el usuario para mostrar en el mensaje de confirmación
        usuario = self.vista.obtener_usuario_seleccionado()

        # Confirmar eliminación con el usuario
        import tkinter.messagebox as messagebox
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que quieres eliminar a {usuario.nombre}?"
        )

        if not confirmar:
            return

        try:
            # Eliminar el usuario usando la función del modelo
            self.modelo.eliminar(indice)

            # Actualizar la vista con la lista actualizada
            self.vista.mostrar_usuarios(self.modelo.listar())

            # Limpiar el panel de detalles
            self.vista.mostrar_detalle_usuario(None)

            # Guardar los cambios en el CSV
            try:
                self.modelo.guardar_csv()
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
            except Exception as e:
                messagebox.showwarning("Advertencia", f"Usuario eliminado pero no se pudo guardar en CSV: {str(e)}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el usuario: {str(e)}")

    # Función para editar el usuario
    def editar_usuario(self):
        print("En construcción...")

    # Función que abre una ventana para añadir un usuario
    # Decidí hacerlo así en vez de crear una clase nueva para respetar la estructura de los archivos
    # que nos dieron en la tarea
    def abrir_formulario(self):
        # Crear formulario modal con CTkToplevel
        formulario = ctk.CTkToplevel(self.app)
        formulario.title("Añadir Usuario")
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

        # Título
        titulo = ctk.CTkLabel(formulario, text="Añadir Usuario", font=("Arial", 16, "bold"))
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

        # Función para seleccionar avatar
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
                else:
                    label_preview.configure(image=None, text="Avatar no encontrado")
            except Exception:
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

        # Preview del avatar
        label_preview = ctk.CTkLabel(frame_principal, text="Selecciona un avatar", height=120, fg_color="gray30",
                                     corner_radius=10)
        label_preview.grid(row=9, column=0, sticky="ew", pady=(0, 10))

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
                self.modelo.añadir(nuevo_usuario)
                self.vista.mostrar_usuarios(self.modelo.listar())
                messagebox.showinfo("Éxito", "Usuario añadido correctamente")
                formulario.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el usuario: {str(e)}")

        # Función para mostrar errores temporales
        def mostrar_error(mensaje):
            error_label = ctk.CTkLabel(formulario, text=mensaje, text_color="red")
            error_label.pack()
            formulario.after(3000, error_label.destroy)

        # Botón xonfirmar en el formulario
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
            messagebox.showinfo("Guardar", "Usuarios guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los usuarios: {str(e)}")

    def cargar_usuarios(self):
        try:
            self.modelo.cargar_csv()
            self.vista.mostrar_usuarios(self.modelo.listar())
            messagebox.showinfo("Cargar", "Usuarios cargados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los usuarios: {str(e)}")

    # Función para salir de la app
    def salir_app(self):
        self.app.destroy()