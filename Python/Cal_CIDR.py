import os
import ipaddress
from colorama import Fore, Back, Style

def banner():
    cartel = r"""
       __      _       ___ ___ ___  ___
     / __|__ _| |__   / __|_ _|   \| _ \
    | (__/ _` | / _| | (__ | || |) |   /   
     \___\__,_|_\__|  \___|___|___/|_|_\
                                             
    """
    clear_screen()
    print(Fore.BLUE + cartel)
    print(Fore.BLUE + "************************************************")

# Función para calcular el CIDR (Classless Inter-Domain Routing)
def calculate_cidr():
    while True:
        clear_screen() 
        banner()

        # Solicita al usuario la IP
        ip_string = input(Style.RESET_ALL + "\nIngrese una dirección IP ('n' para terminar): ")

        if ip_string.lower() == "n":
            break

        try:
            # Intenta crear un objeto de red IP a partir de la cadena proporcionada
            ip_network = ipaddress.ip_network(ip_string, strict=False)
            print(f"{ip_network}")  # Muestra la red IP calculada , f para respetar el formato de ip de red
            input(Style.RESET_ALL + "Presione Enter para continuar...")
        except ValueError:
            # Si se produce un error de valor, se vuelve a pedir la IP
            print(Fore.BLACK + Back.RED + "Dirección IP inválida. Inténtelo de nuevo.")
            input(Style.RESET_ALL + "Presione Enter para continuar...")
            continue  # Continúa con la próxima iteración del bucle si hay un error


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    clear_screen()
    calculate_cidr()
