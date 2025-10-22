import tkinter as tk

# Creamos la ventana principal
root = tk.Tk()
root.title("Ejercicio 1: Label")
root.geometry("300x150")

# Creamos la etiqueta con el mensaje que cambiará
etiqueta_mensaje = tk.Label(root, text="¡Holaaaa! ¿qué tal? :)")
etiqueta_mensaje.pack(pady=5)

# Creamos la función para cambiar el mensaje
def mostrar_mensaje():
    etiqueta_mensaje.config(text="Aquí estamos, trabajando duro")

# Creamos el botón que va a cambiar el mensaje
boton_mensaje = tk.Button(root, text="Haz click aquí para mostrar mensaje", command=mostrar_mensaje)
boton_mensaje.pack(pady=5)

# Creamos el botón de salir
boton_cerrar = tk.Button(root, text="Haz click aquí para salir", command=root.quit)
boton_cerrar.pack(pady=5)

root.mainloop()