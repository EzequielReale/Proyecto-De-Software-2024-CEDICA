from src.suma import suma
from src.resta import resta
from src.multiplicacion import multiplicacion
from src.division import division
import sys

def ingresar_datos():
    try:
        a = float(input("Ingrese el primer número: "))
        operation = input("Ingrese la operación a realizar: ")
        b = float(input("Ingrese el segundo número: "))
    except ValueError:
        print("Error: Ingrese un número válido", file=sys.stderr)
        return ingresar_datos()
    except Exception as e:
        print("Error: ", e, file=sys.stderr)
        return ingresar_datos()
    return a, b, operation

def main():
    while True:
        a, b, operation = ingresar_datos()
        print("El resultado es: ")
        if operation == "+":
            print(suma(a, b))
        elif operation == "-":
            print(resta(a, b))
        elif operation == "*":
            print(multiplicacion(a, b))
        elif operation == "/":
            try:
                print(division(a, b))
            except ValueError:
                print("Error: No se puede dividir por 0", file=sys.stderr)
        else:
            print("Operación no válida", file=sys.stderr)

        if input("Desea realizar otra operación? (s/n): ") == "n":
            break

if __name__ == "__main__":
    main()
