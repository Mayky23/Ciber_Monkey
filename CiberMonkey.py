import os
from Python import Cal_CIDR
from Python import Wifi_Scanner
from Python import Dev_IP_act
from Python import Escucha_ports
from Python.ListarSubdominios import sublist3r 
from Python import DDos_atack
from Python import Pswd_generator
from Python.Wifi_pswd.WifiBF import menu
from Python.Wifi_atack import wifiCrack
from Python import Spoofing
from Python import Backdoor
from Python import Encriptar_Desencriptar
from Python import Data_generator
from Python import SQL_injection

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
    print("| 2. WIFI SCANNER                |")
    print("| 3. DESCUBRIR IP ACTIVA         |")
    print("| 4. ESCUCHA DE PUERTOS          |")
    print("| 5. LISTAR SUBDOMINIOS          |")
    print("| 6. ATAQUE DDoS                 |")
    print("| 7. CREAR CONTRASEÑA            |")
    print("| 8. CRACKEAR PSWD WIFI          |")
    print("| 9. ATACAR WIFI                 |")
    print("| 10. SPOOFING                   |")
    print("| 11. BACK DOOR                  |")
    print("| 12. EN / DESENCRIPTAR ARCHIVO  |")
    print("| 13. GENERAR DATOS              |")
    print("| 14. INYECCIÓN SQL              |")
    print("| 15. AUDITAR BD SQL (disabled)  |")
    print("|--------------------------------|")
    print("| 99. SALIR DEL PROGRAMA         |")
    print("==================================")

def main():
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

def switch_options(option):
    options_dict = {
        1: Cal_CIDR,
        2: Wifi_Scanner,
        3: Dev_IP_act,
        4: Escucha_ports,
        5: sublist3r,
        6: DDos_atack,
        7: Pswd_generator,
        8: menu,
        9: wifiCrack,
        10: Spoofing,
        10: Backdoor,
        11: Encriptar_Desencriptar,
        12: Data_generator,
        13: SQL_injection,
        # 14: mysql_audit_main,
        99: print("SALIENDO DEL PROGRAMA...")
    }
    func = options_dict.get(option)
    if func:
        func()
    else:
        print("Opción no válida.")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    print_ascii_art()
    print_menu()

if __name__ == "__main__":
    main()
