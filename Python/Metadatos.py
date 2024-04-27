import exifread
import os
from colorama import *

def obtener_metadatos_imagen(ruta_imagen):
    try:
        with open(ruta_imagen, 'rb') as imagen:
            tags = exifread.process_file(imagen)
            print("Metadatos de la imagen:")
            for tag, valor in tags.items():
                print(f"{tag}: {valor}")
    except FileNotFoundError:
        print(Fore.BLACK + Back.RED + "¡Archivo no encontrado!"  + Style.RESET_ALL)
    except Exception as e:
        print(Fore.BLACK + Back.RED + f"Ocurrió un error: {e}" + Style.RESET_ALL)

def obtener_metadatos_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
            print("Contenido del archivo:")
            print(contenido)
    except FileNotFoundError:
        print(Fore.BLACK + Back.RED + "¡Archivo no encontrado!"  + Style.RESET_ALL)
    except Exception as e:
        print(Fore.BLACK + Back.RED + f"Ocurrió un error: {e}" + Style.RESET_ALL)

def main():
    banner()
    print("\n************************")
    print("*   TIPO DE ARCHIVO :  *")
    print("************************")
    print("*      1. FOTO         *")
    print("*                      *")
    print("*      2. DOCUMENTO    *")
    print("************************")

    opcion = input(Style.RESET_ALL + "\nSeleccione el tipo de archivo (1/2) o n para salir: ").strip()

    if opcion.lower() == 'n':
        return  # Salir del programa si se ingresa 'n'
    if opcion == '1':
        ruta_imagen = input("Ruta de la imagen: ")
        obtener_metadatos_imagen(ruta_imagen)
    elif opcion == '2':
        ruta_archivo = input("Ruta del archivo: ")
        obtener_metadatos_archivo(ruta_archivo)
    else:
        print(Fore.BLACK + Back.RED + "Opción no válida." + Style.RESET_ALL)

def banner():
    cartel = r"""
  __  __     _          ___           
 |  \/  |___| |_ __ _  / __|_ __ _  _ 
 | |\/| / -_)  _/ _` | \__ \ '_ \ || |
 |_|  |_\___|\__\__,_| |___/ .__/\_, |
                           |_|   |__/ 
    """
    clear_screen()
    print(Fore.CYAN + cartel)
    print(Fore.CYAN + "************************************************")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    main()