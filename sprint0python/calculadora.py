import operaciones

import operaciones

while True:
    print("Escribe dos números")
    n1 = int(input())
    n2 = int(input())

    print("¿Qué operación desea realizar? (suma | resta | multiplicación | división)")
    operacion = input()

    if operacion == 'suma':
        print(operaciones.suma(n1, n2))

    elif operacion == 'resta':
        print(operaciones.resta(n1, n2))

    elif operacion == 'multiplicación':
        print(operaciones.multiplicacion(n1, n2))

    elif operacion == 'división':
        print(operaciones.division(n1, n2))

    else:
        print("Introduzca una operación válida\n")
        continue

    print("\n¿Desea realizar otra operación? (sí / no)")
    respuesta = input().lower()

    if respuesta != 'sí':
        print("Programa terminado.")
        break


