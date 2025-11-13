class Usuario:
    def __init__(self, nombre: str, edad: int, genero: str, avatar: str):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.avatar = avatar


class GestorUsuarios:
    def __init__(self):
        self._usuarios = []  # lista de Usuario

    def listar(self):
        return list(self._usuarios)

    def añadir(self, usuario: Usuario):
        # validaciones mínimas (nombre no vacío, edad en rango, genero permitido)
        if not usuario.nombre or not usuario.nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        if usuario.edad < 0 or usuario.edad > 100:
            raise ValueError("La edad debe estar entre 0 y 100")

        generos_permitidos = ["masculino", "femenino", "otro"]
        if usuario.genero not in generos_permitidos:
            raise ValueError(f"Género debe ser uno de: {', '.join(generos_permitidos)}")

        if not usuario.avatar:
            raise ValueError("Debe seleccionar un avatar")

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