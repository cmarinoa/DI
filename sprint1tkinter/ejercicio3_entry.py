import tkinter as tk

# Creamos la ventana principal
root = tk.Tk()
root.title("Ejercicio 1: Label")
root.geometry("300x150")

# Creamos la función para saludar la usuario
def saludar():
    etiqueta_saludo.config(text=f"Buenos días, {entrada.get()}")

# Creamos la etiqueta que cambiará para saludar
etiqueta_saludo = tk.Label(root, text="¿Cömo te llamas?")
etiqueta_saludo.pack(pady=5)

# Creamos el campo de entrada
entrada = tk.Entry(root)
entrada.pack(pady=5)

# Creamos el botón que cambiará el texto
boton_cambiar_texto = tk.Button(root, text="Salúdame", command=saludar)
boton_cambiar_texto.pack(pady=5)

root.mainloop()