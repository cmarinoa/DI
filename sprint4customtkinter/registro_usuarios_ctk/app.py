import customtkinter as ctk
from controller.app_controller import AppController

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    #Le meto un pack personalizado de colores que está en la carpeta themes
    ctk.set_default_color_theme("themes/cherry.json")

    app = ctk.CTk()
    app.title("Registro de Usuarios (CTk + MVC)")
    app.geometry("1000x600")

    controller = AppController(app)  # crea modelo y vista dentro
    app.mainloop()