import exifread
from colorama import Fore, Back, Style
from Python.ui import draw_banner, pause

COMMON_ASCII = r"""
 Meta Spy
"""
BANNER_COLOR = "\033[90m"

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
    print("\n1. Imagen")
    print("2. Documento")

    while True:
        opcion = input(Style.RESET_ALL + "\nSeleccione el tipo de archivo (1/2) o n para salir: ").strip()
        if opcion.lower() == 'n':
            return  # Salir del programa si se ingresa 'n'
        elif opcion == '1':
            ruta_imagen = input("Ruta de la imagen: ")
            obtener_metadatos_imagen(ruta_imagen)
            pause()
            break
        elif opcion == '2':
            ruta_archivo = input("Ruta del archivo: ")
            obtener_metadatos_archivo(ruta_archivo)
            pause()
            break
        else:
            print(Fore.RED + "Opción no válida.")


def banner():
    draw_banner("", COMMON_ASCII, "Imagenes y documentos", BANNER_COLOR)

if __name__ == "__main__":
    metadata_main()
