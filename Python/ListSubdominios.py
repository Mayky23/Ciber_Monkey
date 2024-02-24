import argparse
from Python.Sublist3r import sublist3r
import os
from colorama import *

def List_Subdominios(domain, no_threads=40, savefile=None, ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None):
    """
    Enumera los subdominios de un dominio dado utilizando Sublist3r.

    Args:
        domain (str): El dominio del cual se quieren enumerar los subdominios.
        no_threads (int): Número de hilos para usar durante la enumeración (por defecto 40).
        savefile (str): Nombre del archivo donde guardar la salida (por defecto None).
        ports (str): Lista de puertos TCP separados por comas para escanear (por defecto None).
        silent (bool): Establece Sublist3r para trabajar en modo silencioso durante la ejecución (útil cuando no se necesita mucho ruido) (por defecto False).
        verbose (bool): Muestra los subdominios encontrados en tiempo real (por defecto False).
        enable_bruteforce (bool): Habilita el módulo de fuerza bruta (por defecto False).
        engines (list): (Opcional) para elegir motores específicos (por defecto None).

    Returns:
        set: Conjunto de subdominios únicos encontrados por Sublist3r.
    """
    try:
        subdomains = sublist3r.main(domain, no_threads, savefile, ports, silent, verbose, enable_bruteforce, engines)
        return subdomains
    except Exception as e:
        print(f"Error al enumerar los subdominios: {e}")
        return set()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Enumerar subdominios utilizando Sublist3r")
    parser.add_argument("-d", "--domain", help="Nombre de dominio para enumerar subdominios de", required=True)
    parser.add_argument("-b", "--bruteforce", help="Habilitar el módulo de fuerza bruta", action="store_true")
    parser.add_argument("-p", "--ports", help="Escanear los subdominios encontrados contra puertos TCP específicos", type=str)
    parser.add_argument("-v", "--verbose", help="Habilitar el modo verbose y mostrar resultados en tiempo real", action="store_true")
    parser.add_argument("-t", "--threads", help="Número de hilos a utilizar para la fuerza bruta", type=int, default=40)
    parser.add_argument("-e", "--engines", help="Especificar una lista separada por comas de motores de búsqueda", type=str)
    parser.add_argument("-o", "--output", help="Guardar los resultados en un archivo de texto", type=str)
    return parser.parse_args()

def List_Subdominios_main():
    clear_screen()
    banner()
    args = parse_arguments()
    domain = args.domain
    no_threads = args.threads
    savefile = args.output
    ports = args.ports
    verbose = args.verbose
    enable_bruteforce = args.bruteforce
    engines = None
    if args.engines:
        engines = args.engines.split(',')
    subdomains = List_Subdominios(domain, no_threads, savefile, ports, verbose=verbose, enable_bruteforce=enable_bruteforce, engines=engines)
    if subdomains:
        print(f"Subdominios encontrados para {domain}:")
        for subdomain in subdomains:
            print(subdomain)
    else:
        print("No se encontraron subdominios.")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    cartel = r"""
     ___                 _           ___      _          _   _         
    |   \ ___ _ __  __ _(_)_ _  ___ |   \ ___| |_ ___ __| |_(_)_ _____ 
    | |) / _ \ '  \/ _` | | ' \(_-< | |) / -_)  _/ -_) _|  _| \ V / -_)
    |___/\___/_|_|_\__,_|_|_||_/__/ |___/\___|\__\___\__|\__|_|\_/\___|
                                                                                                             
    """
    clear_screen()
    print(Fore.LIGHTGREEN_EX + cartel)
    print(Fore.LIGHTGREEN_EX + "***********************************************************************"  + Style.RESET_ALL)


if __name__ == "__main__":
    clear_screen()
    banner()
    List_Subdominios_main()
