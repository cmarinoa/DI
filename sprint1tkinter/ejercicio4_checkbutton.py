import tkinter as tk

# Creamos la ventana principal
root = tk.Tk()
root.title("Ejercicio 4: CheckButton")
root.geometry("300x150")

# Definimos las variables
var_leer = tk.IntVar()
var_deporte = tk.IntVar()
var_musica = tk.IntVar()

# Creamos la función para mostrar la selección
def mostrar_seleccion():
    texto = "Aficiones seleccionadas: "

    # ifs anidados para revisar cada variable,
    # 0 = no marcada
    # 1 = marcada
    if var_leer.get() == 1:
        texto += " Leer | "
    if var_deporte.get() == 1:
        texto += "Deporte | "
    if var_musica.get() == 1:
        texto += "Música |"

    # Si no hay ninguna seleccionada:
    if var_leer.get() == 0 and var_deporte.get() == 0 and var_musica.get() == 0:
        texto = "No hay aficiones seleccionadas"

    #Actualizo la etiqueta
    etiqueta.config(text=texto)

# Creo checkbutton para leer
checkbutton_leer = tk.Checkbutton(root, text="Leer", variable=var_leer, command=mostrar_seleccion)
checkbutton_leer.pack(pady=5)

# Creo checkbutton para deporte
checkbutton_deporte = tk.Checkbutton(root, text="Deporte", variable=var_deporte, command=mostrar_seleccion)
checkbutton_deporte.pack(pady=5)

# Creo checkbutton para música
checkbutton_musica = tk.Checkbutton(root, text="Música", variable=var_musica, command=mostrar_seleccion)
checkbutton_musica.pack(pady=5)

#Creo etiqueta que va a ir cambiando según las aficiones seleccionadas
etiqueta = tk.Label(root, text ="No hay aficiones seleccionadas")
etiqueta.pack(pady=5)

root.mainloop()

