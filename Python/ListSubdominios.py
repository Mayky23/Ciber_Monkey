import os
from colorama import *
import sublist3r

# Función para limpiar la pantalla
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Función para imprimir el banner
def banner():
    cartel = r"""
     ___                 _           ___      _          _   _         
    |   \ ___ _ __  __ _(_)_ _  ___ |   \ ___| |_ ___ __| |_(_)_ _____ 
    | |) / _ \ '  \/ _` | | ' \(_-< | |) / -_)  _/ -_) _|  _| \ V / -_)
    |___/\___/_|_|_\__,_|_|_||_/__/ |___/\___|\__\___\__|\__|_|\_/\___|  
    """
    clear_screen()
    print(Fore.MAGENTA + cartel)
    print(Fore.MAGENTA + "***********************************************************************" + Style.RESET_ALL)
    print("Escriba 'n' en cualquier momento para cancelar.\n")

# Función para obtener el dominio del usuario con validación de entrada
def get_domain_from_user():
    while True:
        dominio = input("Introduce el nombre de dominio (sin http/https): ").strip()
        if not dominio:
            print("Error: El dominio no puede estar vacío. Inténtalo de nuevo.")
        elif dominio.lower() == 'n':
            return None
        else:
            return dominio

# Función para obtener la ruta del archivo de resultados del usuario con validación de entrada
def get_savefile_path_from_user():
    while True:
        ruta_archivo = input("Ingresa la ruta donde se guardará el archivo de resultados (el valor predeterminado es 'subdominios.txt'): ").strip()
        if not ruta_archivo:
            ruta_archivo = 'subdominios.txt'  # Valor predeterminado

        # Verificar si el directorio existe o se puede crear
        directorio = os.path.dirname(ruta_archivo)
        try:
            os.makedirs(directorio, exist_ok=True)
        except OSError as e:
            print(Fore.BLACK + Back.RED + f"Error: No se pudo crear el directorio. Detalles: {str(e)}" + Style.RESET_ALL)
            continue

        # Verificar si se tienen permisos para escribir en el directorio
        if not os.access(directorio, os.W_OK):
            print(Fore.BLACK + Back.RED + "Error: No tienes permisos para escribir en la carpeta especificada. Inténtalo de nuevo." + Style.RESET_ALL)
            continue

        return ruta_archivo


# Función para establecer opciones de enumeración de subdominios
def set_options():
    global no_threads, savefile, ports, silent, verbose, enable_bruteforce, engines
    
    # Preguntar por el número de hilos
    no_threads = int(input("Ingresa el número de hilos (el valor predeterminado es 40): ") or "40")

    # Preguntar por la ruta del archivo de guardado
    savefile = get_savefile_path_from_user()
    if savefile is None:
        return False

    # Preguntar por las opciones de escaneo de puertos
    ports_input = input("¿Quieres especificar los puertos a escanear? (s/n): ").lower()
    if ports_input == 's':
        ports = input("Ingresa los puertos a escanear (separados por comas): ").split(',')
    else:
        ports = None

    # Preguntar por el modo silencioso
    silent_input = input("¿Quieres ejecutar en modo silencioso? (s/n): ").lower()
    silent = silent_input == 's'

    # Preguntar por el modo detallado
    verbose_input = input("¿Quieres ejecutar en modo detallado? (s/n): ").lower()
    verbose = verbose_input == 's'

    # Preguntar por la opción de fuerza bruta
    brute_force_input = input("¿Quieres habilitar la fuerza bruta? (s/n): ").lower()
    enable_bruteforce = brute_force_input == 's'

    # Preguntar por los motores de búsqueda personalizados
    engines_input = input("¿Quieres usar motores de búsqueda personalizados? (s/n): ").lower()
    if engines_input == 's':
        engines = input("Ingresa los motores de búsqueda personalizados (separados por comas): ").split(',')
    else:
        engines = None

    return True

# Función principal para la enumeración de subdominios
def List_Subdominios_main():
    clear_screen()
    banner()

    # Obtener el dominio del usuario
    dominio = get_domain_from_user()
    if dominio is None:
        print("Cerrando...")
        return False

    # Establecer opciones para la enumeración de subdominios
    if not set_options():
        return False

    # Encontrar subdominios
    subdominios = sublist3r.main(dominio, no_threads, savefile, ports, silent, verbose, enable_bruteforce, engines)

    # Imprimir subdominios
    print("Subdominios encontrados:")
    for subdominio in subdominios:
        print(subdominio)

    return True

if __name__ == "__main__":
    while List_Subdominios_main():
        pass
