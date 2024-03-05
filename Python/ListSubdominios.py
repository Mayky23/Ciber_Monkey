import os  
from colorama import Fore, Style
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
    print(Fore.LIGHTGREEN_EX + "***********************************************************************"  + Style.RESET_ALL)
    print(cartel)

# Función para obtener el dominio desde la entrada del usuario
def get_domain_from_user():
    clear_screen()
    banner()
    return input("Por favor, introduce el nombre de dominio (sin http/https): ").strip()  # Eliminar espacios alrededor

# Opciones
no_threads = 40
savefile = "subdominios.txt"
ports = None
silent = False
verbose = False
enable_bruteforce = False
engines = None

if __name__ == "__main__":
    clear_screen()
    banner()
    
    # Obtener el dominio del usuario
    dominio = get_domain_from_user()

    # Buscar subdominios
    subdominios = sublist3r.main(dominio, no_threads, savefile, ports, silent, verbose, enable_bruteforce, engines)

    # Imprimir subdominios
    print("Subdominios encontrados:")
    for subdominio in subdominios:
        print(subdominio)

