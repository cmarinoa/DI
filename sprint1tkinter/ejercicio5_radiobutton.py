import tkinter as tk

# Creamos la ventana principal
root = tk.Tk()
root.title("Ejercicio 5: RadioButton")
root.geometry("150x150")

# Función que cambia el color del fondo cuando se pulsa un botón
def cambiar_color():
    # Obtengo el atributo "value" de cada botón
    color = var_radiobutton.get()
    # Aplico el valor de "value" al fondo de la app
    root.config(bg=color)

# Declaro variable de control
var_radiobutton = tk.StringVar()
# Pongo un valor por defecto
var_radiobutton.set("blue")

# Creación de los radiobuttons, 1 por color
radiobutton1 = tk.Radiobutton(root, text="Azul",
                              variable=var_radiobutton,
                              value="blue",
                              command=cambiar_color)
radiobutton1.pack(pady=5)

radiobutton2 = tk.Radiobutton(root, text="Rojo",
                        variable=var_radiobutton,
                        value="red",
                        command=cambiar_color)
radiobutton2.pack(pady=5)

radiobutton3 = tk.Radiobutton(root,text="Verde",
                              variable=var_radiobutton,
                              value="green",
                              command=cambiar_color)
radiobutton3.pack(pady=5)

# Ponemos el color default de fondo a azul
root.config(bg="blue")

root.mainloop()