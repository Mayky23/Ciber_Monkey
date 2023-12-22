import os
from Python.Cal_CIDR import calculate_cidr
from Python.Wifi_Scanner import wifi_scanner_main
from Python.Dev_IP_act import host_discovery_main
from Python.Port_scanner import main as PORTS_Scanner_main
from Python.Escucha_ports import escucha_puertos_main
from Python.DDos_atack import ddos_attack_main
from Python.Pswd_generator import password_generator_main
from Python.Contrasena_Craking.Pswd_Craking import main as Contrasena_Cracking_main
from Python.Encriptar_Desencriptar import encriptar_desencriptar_main
from Python.Data_generator import data_generator_main
from Python.SQL_injection import sql_injection_main
from Python.Auditar_BD import mysql_audit_main


def main():
    option = 0

    while option != 99:
        clear_screen()

        print(" /$$   /$$             /$$           /$$   /$$                       /$$                            ")
        print("| $$$ | $$            | $$          | $$  | $$                      | $$                            ")
        print("| $$$$| $$  /$$$$$$  /$$$$$$        | $$  | $$ /$$   /$$ /$$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$     ")
        print("| $$ $$ $$ /$$__  $$|_  $$_/        | $$$$$$$$| $$  | $$| $$__  $$|_  $$_/   /$$__  $$ /$$__  $$    ")
        print("| $$  $$$$| $$$$$$$$  | $$          | $$__  $$| $$  | $$| $$  \\ $$  | $$    | $$$$$$$$| $$  \\__/  ")
        print("| $$\\  $$$| $$_____/  | $$ /$$      | $$  | $$| $$  | $$| $$  | $$  | $$ /$$| $$_____/| $$         ")
        print("| $$ \\  $$|  $$$$$$$  |  $$$$/      | $$  | $$|  $$$$$$/| $$  | $$  |  $$$$/|  $$$$$$$| $$         ")
        print("|__/  \\__/ \\_______/   \\___/        |__/  |__/ \\______/ |__/  |__/   \\___/   \\_______/|__/    ")

        print("\n -By: MARH--------------------------------------------------------------------------------------")

        print("\n==================================")
        print("| 1. CALCULAR CIDR               |")
        print("| 2. MOSTRAR REDES WIFI          |")
        print("| 3. DESCUBRIR IP ACTIVA         |")
        print("| 4. ESCANEAR PUERTOS            |")
        print("| 5. ESCUCHA DE PUERTOS          |")
        print("| 6. ATAQUE DDoS                 |")
        print("| 7. CREAR CONTRASEÑA            |")
        print("| 8. CRACKEAR CONTRASEÑA         |")
        print("| 9. EN / DESENCRIPTAR ARCHIVO   |")
        print("| 11. GENERAR DATOS              |")
        print("| 13. INYECCIÓN SQL              |")
        print("| 14. AUDITAR BD SQL             |")
        print("|--------------------------------|")
        print("| 99. SALIR DEL PROGRAMA         |")
        print("==================================")
        print("\nSELECCIONA UNA OPCIÓN: ")

        try:
            option = int(input())
        except ValueError:
            print("Por favor, ingresa un número válido.")
            continue

        switch_options(option)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def switch_options(option):
    options_dict = {
        1: calculate_cidr,
        2: wifi_scanner_main, 
        3: host_discovery_main,
        4: PORTS_Scanner_main,
        5: escucha_puertos_main,
        6: ddos_attack_main, 
        7: password_generator_main,
        8: Contrasena_Cracking_main,
        9: encriptar_desencriptar_main,
        11: data_generator_main,
        13: sql_injection_main,
        # 14: mysql_audit_main,
        99: lambda: print("SALIENDO DEL PROGRAMA...\n----------------------------------\n|          By: MARH              |\n----------------------------------")
    }

    try:
        func = options_dict.get(option, lambda: print("OPCIÓN INVÁLIDA, INTÉNTALO DE NUEVO"))
        print("----------------------------------")
        func()
        print("----------------------------------")

        if option != 99:
            input("PRESIONA ENTER PARA CONTINUAR")
    except Exception as e:
        print(f"Se produjo un error: {e}")


if __name__ == "__main__":
    main()