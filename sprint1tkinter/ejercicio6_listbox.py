import tkinter as tk

# Creamos la ventana principal
root = tk.Tk()
root.title("Ejercicio 6: Listbox")
root.geometry("300x300")

# Función para mostrar las frutas seleccionadas
def mostrar_frutas():
    seleccion = listbox.curselection()
    frutas = [listbox.get(i) for i in seleccion]
    etiqueta.config(text=f"Seleccionaste: {', '.join(frutas)}")

# Creo lista de frutas
frutas = ["Manzana", "Banana", "Naranja"]

# Creo listbox y recorro la lista de frutas para rellenarlo
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
for fruta in frutas:
    listbox.insert(tk.END, fruta)
listbox.pack(pady=5)

# Creo el botón de mostrar frutas y lo conecto a la función
boton = tk.Button(root, text="Mostrar frutas", command=mostrar_frutas)
boton.pack(pady=5)

# Creo la etiqueta que mostrará las frutas seleccionadas
etiqueta = tk.Label(root, text="Seleccionaste: Ninguno")
etiqueta.pack(pady=5)

root.mainloop()
