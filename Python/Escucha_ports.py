import os
import socket
import subprocess

from colorama import *

def escucha_puertos(puerto, direccion_ip):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((direccion_ip, puerto))
        server_socket.listen(1)
        print("-----------------------------------------------------------")
        print(Style.RESET_ALL + f"Esperando conexiones entrantes en {direccion_ip}:{puerto}...")

        client_socket, addr = server_socket.accept()
        print(Style.RESET_ALL + f"Conexión establecida desde: {addr[0]}:{addr[1]}")

        # Obtener información de la conexión entrante
        peer_ip, peer_port = client_socket.getpeername()
        print(Style.RESET_ALL + f"Conexión entrante desde: {peer_ip}:{peer_port}")

        isocket = client_socket.makefile("r")
        osocket = client_socket.makefile("w")

        while True:
            command = isocket.readline().strip()

            if command.lower() == "exit":
                break

            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            process.wait()

            command_output = process.stdout.read()
            osocket.write(command_output)
            osocket.flush()

        client_socket.close()
        server_socket.close()

    except (socket.error, ValueError, subprocess.CalledProcessError) as e:
        print(f"Ocurrió un error: {e}")
        input(Style.RESET_ALL + "Presione Enter para continuar...")
        clear_screen()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def escucha_puertos_main():

    clear_screen()
    
    banner()

    try:
        desea_escuchar = input(Style.RESET_ALL + "¿Desea escuchar puertos? (s/n): ")

        if desea_escuchar.lower() != 's':
            return

        while True:
            direccion_ip = input(Style.RESET_ALL + "Ingrese la dirección IP en la que desea estar a la escucha: ")
            try:
                socket.inet_aton(direccion_ip)
                break
            except socket.error:
                print(Fore.BLACK + Back.RED + "Error: Dirección IP inválida. Inténtelo de nuevo.")
                input(Style.RESET_ALL + "Presione Enter para continuar...")
                clear_screen()
                banner()
                continue  # Volver a solicitar una dirección IP válida

        puerto = int(input(Style.RESET_ALL + "Ingrese el puerto en el que desea estar a la escucha: "))

        escucha_puertos(puerto, direccion_ip)

    except ValueError:
        print(Fore.BLACK + Back.RED + "Error: Puerto inválido. Ingrese un número entero válido.")

def banner():
    cartel = r"""
   ___         _     _    _    _                    
  | _ \___ _ _| |_  | |  (_)__| |_ ___ _ _  ___ _ _ 
  |  _/ _ \ '_|  _| | |__| (_-<  _/ -_) ' \/ -_) '_|
  |_| \___/_|  \__| |____|_/__/\__\___|_||_\___|_|  
                                       
    """
    clear_screen()
    print(Fore.LIGHTGREEN_EX + cartel)
    print("***********************************************************")

if __name__ == "__main__":
    clear_screen()
    escucha_puertos_main()
