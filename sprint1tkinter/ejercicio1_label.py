import tkinter as tk

# Creamos la ventana principal
root = tk.Tk()
root.title("Ejercicio 1: Label")
root.geometry("300x150")

# Crear etiqueta bienvenida
etiqueta_bienvenida = tk.Label(root, text="Bienvenido a mi sprint:)")
etiqueta_bienvenida.pack(pady=5)

# Crear etiqueta nombre
etiqueta_nombre = tk.Label(root, text="Mi nombre es Carmen Mariño Arestín")
etiqueta_nombre.pack(pady=5)

# Crear la etiqueta que va a cambiar
etiqueta_cambiante = tk.Label(root, text="Este texto va a cambiar")
etiqueta_cambiante.pack(pady=5)

# Crear función que hará que cambie la etiqueta
def cambiar_etiqueta():
    etiqueta_cambiante.config(text="¡Adiós!")

# Crear botón que va a ser pulsado para cambiar la etiqueta
boton_cambiar_texto = tk.Button(root, text="Haz click aquí", command=cambiar_etiqueta)
boton_cambiar_texto.pack(pady=5)


root.mainloop()

