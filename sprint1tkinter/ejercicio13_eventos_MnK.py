import tkinter as tk

# Función que recoge los eventos del ratón y crea el círculo en base a ellos
def dibujar_circulo(event):
    x, y = event.x, event.y
    r = 20 # Radio por default
    canvas.create_oval(x - r, y - r, x + r, y + r, outline="blue")

# Función que recoge el evento del teclado cuando se pulsa la tecla c y borra el canvas
def borrar_canvas(event):
    if event.char == "c":
        canvas.delete("all")

# Creo la ventana principal
root = tk.Tk()
root.title("Ejercicio 13: Eventos de teclado y ratón")
root.geometry("500x500")

# Creo el canvas
canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack(pady=5)

# Detecto el click y lo asocio a la función de dibujar el círculo
canvas.bind("<Button-1>", dibujar_circulo)

# Detecto el tecleo y lo asocio a la función de borrar el canvas
root.bind("<Key>", borrar_canvas)

root.mainloop()