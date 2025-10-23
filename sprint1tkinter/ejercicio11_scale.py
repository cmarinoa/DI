import tkinter as tk

# Función para actualizar el valor de la etiqueta
def actualizar_valor(val):
    etiqueta.config(text=f"Valor: {val}")

# Creo ventana principal
root = tk.Tk()
root.title("Ejemplo de Scale")
root.geometry("300x200")

# Creo la escala y le doy los valores del 0 al 100
scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=actualizar_valor)
scale.pack(pady=20)

# Creo la etiqueta y le doy el valor por defecto de 0
etiqueta = tk.Label(root, text="Valor: 0")
etiqueta.pack(pady=10)

root.mainloop()