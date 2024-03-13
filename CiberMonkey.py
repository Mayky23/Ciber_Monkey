import os
import subprocess
import sys
import time
from colorama import *

# Importar los módulos
from Python.Cal_CIDR import calculate_cidr
from Python.Wifi_Scanner import wifi_scanner_main
from Python.Dev_IP_act import host_discovery_main
from Python.Escucha_ports import escucha_puertos_main
from Python.ListSubdominios import List_Subdominios_main
from Python.DDos_atack import ddos_attack_main
from Python.Pswd_generator import password_generator_main
from Python.Encriptar_Desencriptar import encriptar_desencriptar_main
from Python.Data_generator import data_generator_main
from Python.SQL_injection import sql_injection_main


def print_ascii_art():
    clear_screen()
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
    print("| 5. LISTAR SUBDOMINIOS          |")
    print("| 6. ATAQUE DDoS                 |")
    print("| 7. CREAR CONTRASEÑA            |")
    print("| 8. EN / DESENCRIPTAR ARCHIVO   |")
    print("| 9. GENERAR DATOS               |")
    print("| 10. INYECCIÓN SQL              |")
    print("| 11. AUDITAR BD SQL (disabled)  |")
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
        5: List_Subdominios_main,
        6: ddos_attack_main,
        7: password_generator_main,
        8: encriptar_desencriptar_main,
        9: data_generator_main,
        10: sql_injection_main,
        #   11: sql_injection_main,
        99: salir
    }
    func = options_dict.get(option)
    if func:
        func()
    else:
        print(Fore.BLACK + Back.RED + "Opción no válida." + Style.RESET_ALL)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def install_dependencies(dependencies):
    clear_screen()
    installed_packages = subprocess.check_output(['pip', 'freeze']).decode('utf-8').split('\n')
    required_packages = [dependency.split('==')[0] for dependency in dependencies]

    print("[-] Verificando dependencias...")
    missing_dependencies = []

    for dependency in required_packages:
        if dependency not in installed_packages:
            missing_dependencies.append(dependency)

    if not missing_dependencies:
        print(Fore.GREEN + "[-] Todas las dependencias ya están instaladas." + Style.RESET_ALL)
        time.sleep(1)
    else:
        print(Fore.YELLOW + "\n[!] Las siguientes dependencias faltan por instalar:" + Style.RESET_ALL)
        print("____________________________________________________")
        
        for dependency in missing_dependencies:
            print("\n -" ,dependency)
        time.sleep(1)

        total_dependencies = len(missing_dependencies)
        progress_unit = 100 / total_dependencies
        progress = 0

        for index, dependency in enumerate(missing_dependencies, start=1):
            print(Fore.RESET + "\nInstalando dependencia {} de {}...".format(index, total_dependencies))
            try:
                subprocess.check_output(['pip', 'install', dependency])
            except subprocess.CalledProcessError:
                print(Fore.RED + f"No se pudo instalar la dependencia: {dependency}" + Style.RESET_ALL)

            # Simular progreso
            time.sleep(1)

            # Actualizar la barra de progreso
            progress += progress_unit
            bar_length = 20
            bar = "=" * int(progress / (100 / bar_length))
            spaces = " " * (bar_length - len(bar))
            percent = "{}%".format(int(progress))
            print("\rProgreso: [{}{}] {}".format(bar, spaces, percent.rjust(4)), end='', flush=True)
            time.sleep(5)

        print(Fore.RESET + Back.GREEN + "\nTodas las dependencias se han instalado correctamente." + Style.RESET_ALL)
    return True

def main():
    dependencies = ["colorama"]
    if install_dependencies(dependencies):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
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


if __name__ == "__main__":
    main()
