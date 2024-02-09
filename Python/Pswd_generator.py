import secrets
import os
from colorama import *

CARACTERES_MINUSCULAS = "abcdefghijklmnopqrstuvwxyz"
CARACTERES_MAYUSCULAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMEROS = "0123456789"
CARACTERES_ESPECIALES = "!@#$%^&*()_+-=[]{}|;':\"<>,.?/~`"

def generar_contrasena(longitud, opciones):
    caracteres_usados = ""

    if "min" in opciones:
        caracteres_usados += CARACTERES_MINUSCULAS
    if "may" in opciones:
        caracteres_usados += CARACTERES_MAYUSCULAS
    if "num" in opciones:
        caracteres_usados += NUMEROS
    if "esp" in opciones:
        caracteres_usados += CARACTERES_ESPECIALES

    contrasena = ''.join(secrets.choice(caracteres_usados) for _ in range(longitud))
    return contrasena

def password_generator_main():

    clear_screen()
    banner()
    while True:
        opcion = input(Style.RESET_ALL + "¿Desea generar una contraseña? (s/n): ")

        if opcion.lower() == "s":
            while True:
                try:
                    longitud = int(input("\nIngrese la longitud de la contraseña: "))
                    if longitud <= 0:
                        raise ValueError
                    break
                except ValueError:
                    print(Fore.BLACK + Back.RED + "Longitud inválida. Por favor, ingrese un número entero positivo.")
                    print(Style.RESET_ALL + "")

            while True:
                opciones = input("Ingrese las opciones (min/may/num/esp): ").lower().split('/')
                if all(opcion in ["min", "may", "num", "esp"] for opcion in opciones):
                    break
                else:
                    print(Fore.BLACK + Back.RED + "Opciones inválidas. Por favor, ingrese opciones válidas.")
                    print(Style.RESET_ALL + "")
            
            contrasena = generar_contrasena(longitud, opciones)

            print(Fore.LIGHTYELLOW_EX + "-------------------------------------------------------------------")
            print(Style.RESET_ALL + f"La contraseña generada es: {contrasena}")
            print(Fore.LIGHTYELLOW_EX + "-------------------------------------------------------------------")

        elif opcion.lower() == "n":
            break

        else:
            print(Fore.BLACK + Back.RED + "Opción inválida. Inténtelo de nuevo.")
            print(Style.RESET_ALL + "")


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

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    clear_screen()
    banner()
    password_generator_main()
