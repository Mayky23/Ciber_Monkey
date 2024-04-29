import exifread
import os
from colorama import Fore, Back, Style

def obtener_metadatos_imagen(ruta_imagen):
    try:
        with open(ruta_imagen, 'rb') as imagen:
            tags = exifread.process_file(imagen)
            print(Fore.GREEN + "Metadatos de la imagen:")
            for tag, valor in tags.items():
                print(f"{tag}: {valor}")
    except FileNotFoundError:
        print(Fore.RED + "¡Archivo no encontrado!")
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error: {e}")

def obtener_metadatos_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'rb') as archivo:
            contenido = archivo.read().decode('utf-8', errors='ignore')
            print(Fore.GREEN + "Contenido del archivo:")
            print(contenido)
    except FileNotFoundError:
        print(Fore.RED + "¡Archivo no encontrado!")
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error: {e}")


def metadata_main():
    banner()
    print("\n************************")
    print("*   TIPO DE ARCHIVO :  *")
    print("************************")
    print("*      1. FOTO         *")
    print("*                      *")
    print("*      2. DOCUMENTO    *")
    print("************************")

    while True:
        opcion = input(Style.RESET_ALL + "\nSeleccione el tipo de archivo (1/2) o n para salir: ").strip()
        if opcion.lower() == 'n':
            return  # Salir del programa si se ingresa 'n'
        elif opcion == '1':
            ruta_imagen = input("Ruta de la imagen: ")
            obtener_metadatos_imagen(ruta_imagen)
            break
        elif opcion == '2':
            ruta_archivo = input("Ruta del archivo: ")
            obtener_metadatos_archivo(ruta_archivo)
            break
        else:
            print(Fore.RED + "Opción no válida.")


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
    metadata_main()
