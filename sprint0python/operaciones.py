# Ejercicio 0:

# La expresión if __name__ == "__main__" tiene el propósito de controlar
# si un archivo de Python se está ejecutando directamente o si se está
# importando como módulo en otro archivo permitiendo que el código dentro
# de ese bloque solo se ejecite si el archivo no ha sido importado.


#Ejercicio 1;

def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    if b == 0:
        raise ZeroDivisionError
    else:
        return a / b

