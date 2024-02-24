import os
from Python.Cal_CIDR import calculate_cidr
from Python.Wifi_Scanner import wifi_scanner_main
from Python.Dev_IP_act import host_discovery_main
from Python.Escucha_ports import escucha_puertos_main
from Python.Wifi_pswd.WifiBF import crack_wifi_pswd_main
from Python.ListSubdominios import List_Subdominios_main
from Python.DDos_atack import ddos_attack_main
from Python.Pswd_generator import password_generator_main
from Python.Encriptar_Desencriptar import  encriptar_desencriptar_main
from Python.Data_generator import data_generator_main
from Python.SQL_injection import sql_injection_main

import re
from colorama import *

def print_ascii_art():
    ascii_art = r"""
     ___  _  _                 __  __             _              
    / __|(_)| |__  ___  _ _   |  \/  | ___  _ _  | |__ ___  _  _ 
   | (__ | || '_ \/ -_)| '_|  | |\/| |/ _ \| ' \ | / // -_)| || |
    \___||_||_.__/\___||_|    |_|  |_|\___/|_||_||_\_\\___| \_, |
                                                             _| |
    ---- By: MARH ------------------------------------------|__/ 
    """
    lines = ascii_art.split('\n')  # Dividir el arte ASCII en líneas individuales
    colors = [
        Fore.LIGHTMAGENTA_EX,
        Fore.LIGHTMAGENTA_EX,
        Fore.MAGENTA,
        Fore.BLUE,
        Fore.LIGHTBLUE_EX,
        Fore.CYAN,
        Fore.LIGHTCYAN_EX,
        Fore.CYAN,
        Fore.BLUE,
        Fore.LIGHTBLUE_EX,
        Fore.LIGHTMAGENTA_EX
    ]

    #  Iterar sobre cada línea y su respectivo color
    for line, color in zip(lines, colors * (len(lines) // len(colors) + 1)):
        #  Imprimir la línea con el color y estilo BRIGHT
        print(color + Style.BRIGHT + line)

def print_menu():
    print(Fore.BLUE + "|================================|")
    print("| 1. CALCULAR CIDR               |")
    print("| 2. WIFI SCANNER                |")
    print("| 3. DESCUBRIR IP ACTIVA         |")
    print("| 4. ESCUCHA DE PUERTOS          |")
    print("| 5. CRACKEAR PSWD WIFI          |")
    print("| 6. LISTAR SUBDOMINIOS          |")
    print("| 7. ATAQUE DDoS                 |")
    print("| 8. CREAR CONTRASEÑA            |")
    print("| 9. EN / DESENCRIPTAR ARCHIVO   |")
    print("| 10. GENERAR DATOS              |")
    print("| 11. INYECCIÓN SQL              |")
    print("| 12. AUDITAR BD SQL (disabled)  |")
    print("|--------------------------------|")
    print("| 99. SALIR DEL PROGRAMA         |")
    print("|================================|")


def salir():
    ascii_art = r"""
         ___   _   _    ___ ___ _  _ ___   ___           
        / __| /_\ | |  |_ _| __| \| |   \ / _ \          
        \__ \/ _ \| |__ | || _|| .  | |) | (_) |   _   _ 
        |___/_/ \_\____|___|___|_|\_|___/ \___(_) (_) (_)

        * Linkedin: https://www.linkedin.com/in/mardh   
        * GitHub: https://github.com/Mayky23 
                                                  
    """
    print(ascii_art)

def switch_options(option):
    options_dict = {
        1: calculate_cidr,
        2: wifi_scanner_main,
        3: host_discovery_main,
        4: escucha_puertos_main,
        5: crack_wifi_pswd_main,
        6: List_Subdominios_main,
        7: ddos_attack_main,
        8: password_generator_main,
        9: encriptar_desencriptar_main,
        10: data_generator_main,
        11: sql_injection_main,
    #   12: sql_injection_main,
        99: salir
    }
    func = options_dict.get(option)
    if func:
        func()
    else:
        print(Fore.BLACK + Back.RED + "Opción no válida." + Style.RESET_ALL)

def main():
    while True:    
        try:
            clear_screen()
            print_ascii_art()
            print_menu()

            option = int(input("\nSELECCIONA UNA OPCIÓN: " + Fore.RESET))
            if option == 99:
                salir()
                break
            switch_options(option)
        except ValueError:
            print(Fore.BLACK + Back.RED + "Por favor, ingresa un número válido." + Style.RESET_ALL)
            continue


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    main()
