import csv

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

    # Eliminar el usuario cuya posición en la lista coincida con el índice pasado
    def eliminar(self, indice: int):
        # controlar índices fuera de rango
        if indice < 0 or indice >= len(self._usuarios):
            raise IndexError("Índice de usuario fuera de rango")
        self._usuarios.pop(indice)

    # Función para actualizar
    def actualizar(self, indice: int, usuario_actualizado: Usuario):
        if indice < 0 or indice >= len(self._usuarios):
            raise IndexError("Índice de usuario fuera de rango")

        # Validar el usuario actualizado antes de reemplazar
        if not usuario_actualizado.nombre or not usuario_actualizado.nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        if usuario_actualizado.edad < 0 or usuario_actualizado.edad > 100:
            raise ValueError("La edad debe estar entre 0 y 100")

        generos_permitidos = ["masculino", "femenino", "otro"]
        if usuario_actualizado.genero not in generos_permitidos:
            raise ValueError(f"Género debe ser uno de: {', '.join(generos_permitidos)}")

        if not usuario_actualizado.avatar:
            raise ValueError("Debe seleccionar un avatar")

        self._usuarios[indice] = usuario_actualizado

    # función para guardar el csv
    def guardar_csv(self, ruta: str = "usuarios.csv"):
        # csv.writer, utf-8, newline='', try/except
        try:
            with open(ruta, 'w', encoding='utf-8', newline='') as archivo:
                writer = csv.writer(archivo)
                # Escribir cabecera
                writer.writerow(['nombre', 'edad', 'genero', 'avatar'])

                # Escribir cada usuario
                for usuario in self._usuarios:
                    writer.writerow([
                        usuario.nombre,
                        usuario.edad,
                        usuario.genero,
                        usuario.avatar
                    ])
        except PermissionError:
            raise PermissionError(f"No se puede escribir en el archivo {ruta}. Verifique los permisos.")
        except Exception as e:
            raise Exception(f"Error inesperado al guardar: {str(e)}")

    def cargar_csv(self, ruta: str = "usuarios.csv"):
        # limpia y repuebla _usuarios; maneja FileNotFoundError y filas corruptas
        try:
            # Limpiar lista actual
            self._usuarios.clear()

            with open(ruta, 'r', encoding='utf-8', newline='') as archivo:
                reader = csv.reader(archivo)

                # Saltar cabecera
                next(reader, None)

                # Contador para identificar filas con error
                num_fila = 1
                usuarios_cargados = 0

                for fila in reader:
                    num_fila += 1

                    # Verificar que la fila tenga exactamente 4 campos
                    if len(fila) != 4:
                        print(
                            f"Advertencia: Fila {num_fila} ignorada - formato incorrecto (esperados 4 campos, encontrados {len(fila)})")
                        continue

                    try:
                        nombre, edad_str, genero, avatar = fila

                        # Validar y convertir edad
                        if not edad_str.isdigit():
                            print(f"Advertencia: Fila {num_fila} ignorada - edad no válida: '{edad_str}'")
                            continue

                        edad = int(edad_str)

                        # Validaciones básicas
                        if not nombre.strip():
                            print(f"Advertencia: Fila {num_fila} ignorada - nombre vacío")
                            continue

                        if edad < 0 or edad > 100:
                            print(f"Advertencia: Fila {num_fila} ignorada - edad fuera de rango: {edad}")
                            continue

                        generos_permitidos = ["masculino", "femenino", "otro"]
                        if genero not in generos_permitidos:
                            print(f"Advertencia: Fila {num_fila} ignorada - género no válido: '{genero}'")
                            continue

                        if not avatar:
                            print(f"Advertencia: Fila {num_fila} ignorada - avatar vacío")
                            continue

                        # Crear y añadir usuario
                        usuario = Usuario(nombre.strip(), edad, genero, avatar)
                        self._usuarios.append(usuario)
                        usuarios_cargados += 1

                    except Exception as e:
                        print(f"Advertencia: Fila {num_fila} ignorada - error procesando datos: {str(e)}")
                        continue

                print(f"CSV cargado correctamente: {usuarios_cargados} usuarios cargados")

        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
        except PermissionError:
            raise PermissionError(f"No se puede leer el archivo {ruta}. Verifica los permisos.")
        except Exception as e:
            raise Exception(f"Error inesperado al cargar: {str(e)}")