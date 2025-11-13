import customtkinter as ctk
from view.main_view import MainView
from model.usuario_model import GestorUsuarios
import tkinter.messagebox as messagebox

class AppController:
    def __init__(self, app):
        self.app = app
        self.modelo = GestorUsuarios()

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
        print("En construcción...")

    # Función para editar el usuario
    def editar_usuario(self):
        print("En construcción...")

    # Función que abre una ventana para añadir un usuario
    def abrir_formulario(self):
        print("En construcción...")

    def guardar_usuarios(self):
        try:
            self.modelo.guardar_csv()
            messagebox.showinfo("Guardar", "Usuarios guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los usuarios:\n{e}")

    def cargar_usuarios(self):
        try:
            self.modelo.cargar_csv()
            self.vista.mostrar_usuarios(self.modelo.listar())
            messagebox.showinfo("Cargar", "Usuarios cargados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los usuarios:\n{e}")

    # Función para salir de la app
    def salir_app(self):
        self.app.destroy()
