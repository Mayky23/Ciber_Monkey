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

def calculate_cidr():
    while True:
        clear_screen()  
        banner()
        ip_string = input(Style.RESET_ALL + "\nIngrese una dirección IP ('n' para terminar): ")

        if ip_string.lower() == "n":
            break

        try:
            ip_network = ipaddress.ip_network(ip_string, strict=False)
            print(f"{ip_network}")
            input(Style.RESET_ALL + "Presione Enter para continuar...")
        except ValueError:
            print(Fore.BLACK + Back.RED + "Dirección IP inválida. Inténtelo de nuevo.")
            input(Style.RESET_ALL + "Presione Enter para continuar...")
            continue  

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    clear_screen()
    calculate_cidr()
