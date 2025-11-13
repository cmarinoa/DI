class Usuario:
    def __init__(self, nombre: str, edad: int, genero: str, avatar: str):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.avatar = avatar  # ruta relativa en assets/

class GestorUsuarios:
    def __init__(self):
        self._usuarios = []  # lista de Usuario

    def listar(self):
        return list(self._usuarios)

    def añadir(self, usuario: Usuario):
        # validaciones mínimas (nombre no vacío, edad en rango, genero permitido)
        self._usuarios.append(usuario)

    def eliminar(self, indice: int):
        # controlar índices fuera de rango
        ...

    def actualizar(self, indice: int, usuario_actualizado: Usuario):
        ...

    def guardar_csv(self, ruta: str = "usuarios.csv"):
        # csv.writer, utf-8, newline='', try/except
        ...

    def cargar_csv(self, ruta: str = "usuarios.csv"):
        # limpia y repuebla _usuarios; maneja FileNotFoundError y filas corruptas
        ...