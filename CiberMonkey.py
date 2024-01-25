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

def main():
    clear_screen()
    print_ascii_art()
    print_menu()

    while True:
        try:
            option = int(input("\nSELECCIONA UNA OPCIÓN: "))
            if option == 99:
                print("SALIENDO DEL PROGRAMA...")
                break
            switch_options(option)
        except ValueError:
            print("Por favor, ingresa un número válido.")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_ascii_art():
    ascii_art = """
       ____       ___                             ___       ___                  ___                          
      6MMMMb/  68b MM                             `MMb     dMM'                  `MM                          
     8P    YM  Y89 MM                              MMM.   ,PMM                    MM                          
    6M      Y  ___ MM____     ____  ___  __        M`Mb   d'MM   _____  ___  __   MM   __   ____  ____    ___ 
    MM          MM MM'  `Mb 6M'  `Mb MM699         M `Mb d' MM 6M'   `Mb MMM9 `Mb MM  d'  6M'  `Mb `Mb     d' 
    MM          MM MM    MM MM    MM MM'           M  YM.P  MM MM     MM MM'   MM MM d'   MM    MM  YM.  ,P   
    MM          MM MM    MM MMMMMMMM MM            M  `Mb'  MM MM     MM MM    MM MMdM.   MMMMMMMM   MM  M    
    YM      6   MM MM    MM MM       MM            M   YP   MM MM     MM MM    MM MMPYM.  MM         `Mbd'    
      8b    d9  MM MM.  ,M9 YM    d9 MM            M   `'   MM YM.   ,M9 MM    MM MM  YM. YM    d9    YMP     
       YMMMM9  _MM_MYMMMM9   YMMMM9 _MM_          _M_      _MM_ YMMMMM9 _MM_  _MM_MM_  YM._YMMMM9      M      
                                                                                                      d'      
       ----Por: MARH----------------------------------------------------------------------------- (8),P       
                                                                                                   YMM        
    """
    print(ascii_art)

def print_menu():
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
    print("| 14. AUDITAR BD SQL (disabled)  |")
    print("|--------------------------------|")
    print("| 99. SALIR DEL PROGRAMA         |")
    print("==================================")

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
        99: lambda: print("SALIENDO DEL PROGRAMA...")
    }

    try:
        func = options_dict.get(option, lambda: print("OPCIÓN INVÁLIDA, INTÉNTALO DE NUEVO"))
        func()
        if option != 99:
            input("PRESIONA ENTER PARA CONTINUAR")
        clear_screen()
        print_ascii_art()
        print_menu()
    except Exception as e:
        print(f"Se produjo un error: {e}")

if __name__ == "__main__":
    main()
