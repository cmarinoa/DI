import tkinter as tk

class PiedraPapelTijera:
    def __init__(self, root):

        # DEFINIR FRAMES:
        # Voy a hacer un frame para jugador y uno para la máquina para tener
        # las cosas lo más dividido posible y que me sea más fácil hacer cambios.

        # Creo un frame para el jugador donde voy a meter lo que
        # corresponde al jugador
        self.frame_jugador = tk.Frame(root)
        self.frame_jugador.grid(row=1, column=0, pady=15)

        # Ceo un frame para la máquina donde meto lo demás
        self.frame_maquina = tk.Frame(root)
        self.frame_maquina.grid(row=0, column=0, pady=15)

        # Creo un frame para los botones de salir y nuevo juego, porque así
        # se me complica menos el centrarlos
        self.frame_botones = tk.Frame(self.frame_jugador)
        self.frame_botones.grid(row=2, column=0, columnspan=3, pady=15)

        # Creo los botones donde van a ir las imágenes de piedra, papel
        # y tijera
        self.button_j_piedra = tk.Button(self.frame_jugador, text="Piedra")
        self.button_j_piedra.grid(row=0, column=0, padx=25, pady=5, ipady=35, ipadx=35)

        self.button_j_papel = tk.Button(self.frame_jugador, text="Papel")
        self.button_j_papel.grid(row=0, column=1, padx=25, pady=5, ipady=35, ipadx=35)

        self.button_j_tijera = tk.Button(self.frame_jugador, text="Tijera")
        self.button_j_tijera.grid(row=0, column=2, padx=25, pady=5, ipady=35, ipadx=35)

        # Creo los botones de salir del juego y de nuevo juego
        self.button_nuevo = tk.Button(self.frame_botones, text="Nuevo juego", width=12)
        self.button_nuevo.pack(side="left", padx=10)

        self.button_salir = tk.Button(self.frame_botones, text="Salir", width=12)
        self.button_salir.pack(side="left", padx=10)

        # Creo todas las etiquetas que voy a usar en la interfaz
        # Etiquetas para mostrar el contador
        self.etiqueta_jugador_info = tk.Label(self.frame_maquina, text="Jugador")
        self.etiqueta_jugador_info.grid(row=0, column=0, padx=20)

        self.etiqueta_maquina_info = tk.Label(self.frame_maquina, text="Máquina")
        self.etiqueta_maquina_info.grid(row=0, column=1, padx=20)

        # Etiqueta para mostrar el texto de lo que eligió la máquina
        self.etiqueta_eleccion = tk.Label(self.frame_maquina, text="---")
        self.etiqueta_eleccion.grid(row=2, column=2, pady=(5, 0))

        # Etiquetas para mostrar las puntuaciones
        self.etiqueta_puntuacion_jugador = tk.Label(self.frame_maquina, text="0", font=("Arial", 14))
        self.etiqueta_puntuacion_jugador.grid(row=1, column=0, padx=20)

        self.etiqueta_puntuacion_maquina = tk.Label(self.frame_maquina, text="0", font=("Arial", 14))
        self.etiqueta_puntuacion_maquina.grid(row=1, column=1, padx=20)

        # Etiqueta para mostrar la selección de la máquina
        self.etiqueta_e_maquina = tk.Label(self.frame_maquina, text="Elección máquina")
        self.etiqueta_e_maquina.grid(row=0, column=2, padx=30)

        # Hago un recuadro para mostrar la imagen de la elección de la máquina
        self.label_imagen_maquina = tk.Label(
            self.frame_maquina, width=14, height=6,
            relief="ridge", borderwidth=3,
            text="?"
        )
        self.label_imagen_maquina.grid(row=1, column=2, padx=30, pady=(5, 0))

        # Creo las etiquetas que van debajo de cada botón de piedra, papel y tijera
        self.etiqueta_piedra = tk.Label(self.frame_jugador, text="Piedra")
        self.etiqueta_piedra.grid(row=1, column=0)
        self.etiqueta_papel = tk.Label(self.frame_jugador, text="Papel")
        self.etiqueta_papel.grid(row=1, column=1)
        self.etiqueta_tijera = tk.Label(self.frame_jugador, text="Tijera")
        self.etiqueta_tijera.grid(row=1, column=2)

root = tk.Tk()
root.title("Piedra, papel, tijera")
root.geometry("500x400")

juego = PiedraPapelTijera(root)

root.mainloop()