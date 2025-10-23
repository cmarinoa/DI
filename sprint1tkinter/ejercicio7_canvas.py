import tkinter as tk

# Creo la ventana principal
root = tk.Tk()
root.title("Ejercicio 7: Canvas")
root.geometry("500x500")

# Creo el canvas
canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack(pady=5)

# Creo la etiqueta que va a estar asociada a las coordenadas del rectángulo
etiqueta_rectangulo = tk.Label(root, text="Rectángulo (x1, y1, x2, y2):")
etiqueta_rectangulo.pack(pady=5)
# Creo la entrada asociada a dicha etiqueta, por la cual el usuario
# introducirá las coordenadas
entrada_rectangulo = tk.Entry(root)
entrada_rectangulo.pack(pady=5)

# Igual que arriba, pero con el círculo
etiqueta_circulo = tk.Label(root, text="Círculo (x1, y1, x2, y2):")
entrada_circulo = tk.Entry(root)
entrada_circulo = tk.Entry(root)
entrada_circulo.pack(pady=5)

# Creo la función que va a dibujar el rectángulo
def dibujar_rectangulo():
    # Recojo el texto que el usuario escribió en el string e itero sobre él con map(),
    # a continuación, reemplazo las comas que escribe el usuario con espacios y los divido
    # en base a esos espacios, asociándolos en orden a cada una de las variables x1, y1, x2 e y2
    x1, y1, x2, y2 = map(int, entrada_rectangulo.get().replace(",", " ").split())
    canvas.create_rectangle(x1, y1, x2, y2, outline="black")

def dibujar_circulo():
    # Hago lo mismo que hice arriba con el rectángulo pero con el círculo
    x1, y1, x2, y2 = map(int, entrada_circulo.get().replace(",", " ").split())
    canvas.create_oval(x1, y1, x2, y2, outline="blue")

# Botón para proceder al dibujo del rectángulo
boton_rectangulo = tk.Button(root, text="Dibujar rectángulo", command=dibujar_rectangulo)
boton_rectangulo.pack(pady=5)

# Lo mismo que arriba, con el círculo
boton_circulo = tk.Button(root, text="Dibujar círculo", command=dibujar_circulo)
boton_circulo.pack(pady=5)

root.mainloop()