import os
from Cal_CIDR import main as Calculadora_CIDR_main
from Wifi_Scanner import main as Wifi_Scanner_main
from Dev_IP_act import main as Descubrir_Host_main
from Port_scanner import main as PORTS_Scanner_main
from Escucha_ports import main as Escucha_puertos_main
from DDos_atack import main as DDos_Atack_main
from Pswd_generator import main as PasswordGenerator_main
from Contrasena_Cracking import Pswd_Cracking, wordlist
from Encriptar_Desencriptar import main as Encriptador_main
from Data_generator import main as Data_Generator_main
from SQL_injection import main as SQL_Injection_main
from Auditar_BD import main as Auditar_BD_main


def main():
    option = 0

    while option != 15:
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
        print("| 15. SALIR DEL PROGRAMA         |")
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
        1: Calculadora_CIDR_main,
        2: Wifi_Scanner_main,
        3: Descubrir_Host_main,
        4: PORTS_Scanner_main,
        5: Escucha_puertos_main,
        6: DDos_Atack_main,
        7: PasswordGenerator_main,
        8: lambda: Pswd_Cracking(wordlist),
        9: Encriptador_main,
        11: Data_Generator_main,
        13: SQL_Injection_main,
        14: Auditar_BD_main,
        15: lambda: print("SALIENDO DEL PROGRAMA...\n----------------------------------\n|          By: MARH              |\n----------------------------------")
    }

    try:
        func = options_dict.get(option, lambda: print("OPCIÓN INVÁLIDA, INTÉNTALO DE NUEVO"))
        print("----------------------------------")
        func()
        print("----------------------------------")

        if option != 15:
            input("PRESIONA ENTER PARA CONTINUAR")
    except Exception as e:
        print(f"Se produjo un error: {e}")


if __name__ == "__main__":
    main()