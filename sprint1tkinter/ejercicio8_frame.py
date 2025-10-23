import tkinter as tk

# Creo la función para mostrar el contenido de la entrada
# en la etiqueta tras pulsar un botón
def mostrar_entry():
    label1.config(text=entry.get())

# Creo la función para borrar el contenido de dicha etiqueta
def borrar_label():
    label1.config(text="")

# Creo la ventana principal
root = tk.Tk()
root.title("Ejercicio 8: Frame")
root.geometry("300x300")

# Creo el primer frame
frame1 = tk.Frame(root, bg="white", bd=2, relief="sunken")
frame1.pack(padx=20, pady=20, fill="both", expand=True)

# A continuación creo y coloco los widgets del primer frame
label1 = tk.Label(frame1, text="Etiqueta que cambia")
label1.grid(pady=5)

label2 = tk.Label(frame1, text="Escribe algo abajo:")
label2.grid(pady=5)

entry = tk.Entry(frame1, borderwidth=3, relief="sunken")
entry.grid(pady=5)

# Creo segundo frame
frame2 = tk.Frame(root, bg="white", bd=2, relief="sunken")
frame2.pack(padx=20, pady=20, fill="both", expand=True)

# Creo y coloco los widgets del segundo frame
boton1 = tk.Button(frame2, text="Cambiar etiqueta", command=mostrar_entry)
boton1.grid(pady=5)

boton2 = tk.Button(frame2, text="Borrar contenido", command=borrar_label)
boton2.grid(pady=5)

root.mainloop()