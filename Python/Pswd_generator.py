import secrets
import os
from colorama import *

# Definición de conjuntos de caracteres para generar contraseñas.
CARACTERES_MINUSCULAS = "abcdefghijklmnopqrstuvwxyz"
CARACTERES_MAYUSCULAS = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
NUMEROS = "0123456789"
CARACTERES_ESPECIALES = "!@#$%^&*()_+-=[]{}|;':\"<>,.?/~`"

# Función para generar contraseñas aleatorias.
def generar_contrasena(longitud, opciones):
    caracteres_usados = ""

    # Construir el conjunto de caracteres a partir de las opciones seleccionadas.
    if "min" in opciones:
        caracteres_usados += CARACTERES_MINUSCULAS
    if "may" in opciones:
        caracteres_usados += CARACTERES_MAYUSCULAS
    if "num" in opciones:
        caracteres_usados += NUMEROS
    if "espc" in opciones:
        caracteres_usados += CARACTERES_ESPECIALES

    # Generar la contraseña aleatoria utilizando los caracteres definidos.
    contrasena = ''.join(secrets.choice(caracteres_usados) for _ in range(longitud))
    return contrasena

# Función principal para la generación de contraseñas.
def password_generator_main():
    clear_screen()
    banner()
    while True:
        # Solicitar al usuario si desea generar una contraseña.
        opcion = input(Style.RESET_ALL + "¿Desea generar una contraseña? (s/n): ")

        if opcion.lower() == "s":
            while True:
                try:
                    # Solicitar la longitud deseada para la contraseña.
                    longitud = int(input("\nIngrese la longitud de la contraseña: "))
                    if longitud <= 0:
                        raise ValueError
                    break
                except ValueError:
                    # Manejar la excepción en caso de que se ingrese una longitud inválida.
                    print(Fore.BLACK + Back.RED + "Longitud inválida. Por favor, ingrese un número entero positivo.")
                    print(Style.RESET_ALL + "")

            while True:
                # Solicitar las opciones de caracteres deseadas para la contraseña.
                opciones = input("Ingrese las opciones (min/may/num/espc): ").lower().split('/')
                if all(opcion in ["min", "may", "num", "espc"] for opcion in opciones):
                    break
                else:
                    # Manejar la excepción en caso de opciones de caracteres inválidas.
                    print(Fore.BLACK + Back.RED + "Opciones inválidas. Por favor, ingrese opciones válidas.")
                    print(Style.RESET_ALL + "")
            
            # Generar la contraseña utilizando las especificaciones proporcionadas.
            contrasena = generar_contrasena(longitud, opciones)

            # Mostrar la contraseña generada.
            print(Fore.LIGHTYELLOW_EX + "-------------------------------------------------------------------")
            print(Style.RESET_ALL + f"La contraseña generada es: {contrasena}")
            print(Fore.LIGHTYELLOW_EX + "-------------------------------------------------------------------")

        elif opcion.lower() == "n":
            # Salir del bucle si el usuario elige no generar más contraseñas.
            break

        else:
            # Manejar la entrada inválida del usuario.
            print(Fore.BLACK + Back.RED + "\nOpción inválida. Inténtelo de nuevo.")
            print(Style.RESET_ALL + "")


# Función para mostrar el banner de la aplicación.
def banner():
    cartel = r"""
   ___              _                              _           
  | _ \____ __ ____| |  __ _ ___ _ _  ___ _ _ __ _| |_ ___ _ _ 
  |  _(_-< V  V / _` | / _` / -_) ' \/ -_) '_/ _` |  _/ _ \ '_|
  |_| /__/\_/\_/\__,_| \__, \___|_||_\___|_| \__,_|\__\___/_|  
                       |___/                                                                        
    """
    print(Fore.LIGHTRED_EX + cartel)
    print(Fore.LIGHTRED_EX + "***************************************************************")

# Función para limpiar la pantalla de la consola.
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Lógica principal para ejecutar el generador de contraseñas.
if __name__ == "__main__":
    clear_screen()
    banner()
    password_generator_main()
