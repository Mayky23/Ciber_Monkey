# Se importan los módulos necesarios.
import os
import socket
import subprocess

# Se importa la biblioteca colorama para el manejo de colores en la consola.
from colorama import *

# Función para escuchar conexiones en un puerto específico.
def escucha_puertos(puerto, direccion_ip):
    try:
        # Se crea un socket TCP/IP.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Se enlaza el socket al puerto y dirección IP especificados.
        server_socket.bind((direccion_ip, puerto))
        # Se pone el socket en modo de escucha.
        server_socket.listen(1)
        print("-----------------------------------------------------------")
        print(Style.RESET_ALL + f"Esperando conexiones entrantes en {direccion_ip}:{puerto}...")

        # Se acepta la conexión entrante.
        client_socket, addr = server_socket.accept()
        print(Style.RESET_ALL + f"Conexión establecida desde: {addr[0]}:{addr[1]}")

        # Se obtiene información sobre la conexión entrante.
        peer_ip, peer_port = client_socket.getpeername()
        print(Style.RESET_ALL + f"Conexión entrante desde: {peer_ip}:{peer_port}")

        # Se crea un objeto archivo para leer desde el socket.
        isocket = client_socket.makefile("r")
        # Se crea un objeto archivo para escribir en el socket.
        osocket = client_socket.makefile("w")

        # Se espera a recibir comandos del cliente y se ejecutan.
        while True:
            command = isocket.readline().strip()

            if command.lower() == "exit":
                break

            # Se ejecuta el comando en el sistema y se captura la salida.
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            process.wait()

            # Se lee la salida del comando y se envía de vuelta al cliente.
            command_output = process.stdout.read()
            osocket.write(command_output)
            osocket.flush()

        # Se cierran los sockets.
        client_socket.close()
        server_socket.close()

    except (socket.error, ValueError, subprocess.CalledProcessError) as e:
        # Manejo de excepciones en caso de error.
        print(f"Ocurrió un error: {e}")
        input(Style.RESET_ALL + "Presione Enter para continuar...")
        clear_screen()

# Función para limpiar la pantalla de la consola.
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Función principal para interactuar con el usuario y comenzar la escucha de puertos.
def escucha_puertos_main():

    clear_screen()
    
    banner()

    try:
        # Se pregunta al usuario si desea escuchar puertos.
        desea_escuchar = input(Style.RESET_ALL + "¿Desea escuchar puertos? (s/n): ")

        # Si la respuesta no es 's', se termina la función.
        if desea_escuchar.lower() != 's':
            return

        while True:
            # Se solicita al usuario que ingrese la dirección IP en la que desea escuchar.
            direccion_ip = input(Style.RESET_ALL + "Ingrese la dirección IP en la que desea estar a la escucha: ")
            try:
                # Se valida que la dirección IP ingresada sea válida.
                socket.inet_aton(direccion_ip)
                break
            except socket.error:
                # Si la dirección IP es inválida, se muestra un mensaje de error y se vuelve a solicitar.
                print(Fore.BLACK + Back.RED + "Error: Dirección IP inválida. Inténtelo de nuevo.")
                input(Style.RESET_ALL + "Presione Enter para continuar...")
                clear_screen()
                banner()
                continue  # Volver a solicitar una dirección IP válida

        # Se solicita al usuario que ingrese el puerto en el que desea escuchar.
        puerto = int(input(Style.RESET_ALL + "Ingrese el puerto en el que desea estar a la escucha: "))

        # Se inicia la escucha en el puerto y dirección IP especificados.
        escucha_puertos(puerto, direccion_ip)

    except ValueError:
        # Manejo de error si se ingresa un puerto inválido.
        print(Fore.BLACK + Back.RED + "Error: Puerto inválido. Ingrese un número entero válido.")

# Función para mostrar un banner en la consola.
def banner():
    cartel = r"""
   ___         _     _    _    _                    
  | _ \___ _ _| |_  | |  (_)__| |_ ___ _ _  ___ _ _ 
  |  _/ _ \ '_|  _| | |__| (_-<  _/ -_) ' \/ -_) '_|
  |_| \___/_|  \__| |____|_/__/\__\___|_||_\___|_|  
                                       
    """
    clear_screen()
    print(Fore.LIGHTGREEN_EX + cartel)
    print("***********************************************************" + Style.RESET_ALL )

if __name__ == "__main__":
    clear_screen()
    escucha_puertos_main()
