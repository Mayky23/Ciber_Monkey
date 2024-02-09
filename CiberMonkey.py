import os
from Python.Cal_CIDR import calculate_cidr
from Python.Wifi_Scanner import wifi_scanner_main
from Python.Dev_IP_act import host_discovery_main
from Python.Escucha_ports import escucha_puertos_main
from Python.Wifi_pswd.WifiBF import crack_wifi_pswd_main
from Python.Wifi_atack.wifiCrack import wifi_atack_main
from Python.ListarSubdominios.sublist3r import interactive
from Python.DDos_atack import ddos_attack_main
from Python.Pswd_generator import password_generator_main
from Python.Spoofing import Spoofing_main
from Python.Backdoor import backdoor_main
from Python import Encriptar_Desencriptar
from Python import Data_generator
from Python import SQL_injection

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
    print(Fore.CYAN + Style.BRIGHT +  ascii_art)

def print_menu():
    print("==================================")
    print("| 1. CALCULAR CIDR               |")
    print("| 2. WIFI SCANNER                |")
    print("| 3. DESCUBRIR IP ACTIVA         |")
    print("| 4. ESCUCHA DE PUERTOS          |")
    print("| 5. CRACKEAR PSWD WIFI          |")
    print("| 6. ATACAR WIFI                 |")
    print("| 7. LISTAR SUBDOMINIOS          |")
    print("| 8. ATAQUE DDoS                 |")
    print("| 9. CREAR CONTRASEÑA            |")
    print("| 10. SPOOFING                   |")
    print("| 11. BACKDOOR                   |")
    print("| 12. EN / DESENCRIPTAR ARCHIVO  |")
    print("| 13. GENERAR DATOS              |")
    print("| 14. INYECCIÓN SQL              |")
    print("| 15. AUDITAR BD SQL (disabled)  |")
    print("|--------------------------------|")
    print("| 99. SALIR DEL PROGRAMA         |")
    print("==================================")

def main():

    while True:    
        try:
            clear_screen()
            print_ascii_art()
            print_menu()

            option = int(input("\nSELECCIONA UNA OPCIÓN: "))
            if option == 99:
                print("SALIENDO DEL PROGRAMA...")
                break
            switch_options(option)
        except ValueError:
            print("Por favor, ingresa un número válido.")

def switch_options(option):
    options_dict = {
        1: calculate_cidr,
        2: wifi_scanner_main,
        3: host_discovery_main,
        4: escucha_puertos_main,
        5: crack_wifi_pswd_main,
        6: wifi_atack_main,
        7: interactive,
        8: ddos_attack_main,
        9: password_generator_main,
        10: Spoofing_main,
        11: backdoor_main,
        12: Encriptar_Desencriptar,
        13: Data_generator,
        14: SQL_injection,
        # 15: mysql_audit_main,
        99: print("SALIENDO DEL PROGRAMA...")
    }
    func = options_dict.get(option)
    if func:
        func()
    else:
        print(Fore.BLACK + Back.RED + "Opción no válida.")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    main()
