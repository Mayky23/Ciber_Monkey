from __future__ import annotations

import socket
from contextlib import closing

from colorama import Back, Fore, Style, init
from Python.ui import draw_banner, pause

init(autoreset=True)
COMMON_ASCII = r"""
 Port Listener
"""
BANNER_COLOR = "\033[93m"


def banner():
    draw_banner("", COMMON_ASCII, "Listener TCP simple para diagnostico", BANNER_COLOR)


def escucha_puertos(port: int, bind_ip: str) -> None:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((bind_ip, port))
        server_socket.listen(5)
        print(Fore.CYAN + f"Escuchando en {bind_ip}:{port}. Ctrl+C para detener.")

        while True:
            client_socket, addr = server_socket.accept()
            with closing(client_socket):
                print(Fore.GREEN + f"Conexion recibida desde {addr[0]}:{addr[1]}")
                client_socket.sendall(
                    b"Ciber Monkey listener activo. Conexion registrada correctamente.\n"
                )


def escucha_puertos_main():
    while True:
        banner()
        answer = input("Quieres abrir un listener TCP? (s/n): ").strip().lower()
        if answer == "n":
            return
        if answer != "s":
            pause(Fore.RED + "Opcion no valida. Pulsa Enter para continuar...")
            continue

        bind_ip = input("IP local de escucha (ej. 0.0.0.0 o 127.0.0.1): ").strip()
        try:
            socket.inet_aton(bind_ip)
            port = int(input("Puerto de escucha: ").strip())
        except (OSError, ValueError):
            pause(Fore.RED + "IP o puerto no validos. Pulsa Enter para continuar...")
            continue

        try:
            escucha_puertos(port, bind_ip)
        except KeyboardInterrupt:
            pause(Fore.YELLOW + "\nListener detenido. Pulsa Enter para continuar...")
        except OSError as exc:
            pause(Fore.BLACK + Back.RED + f"Error abriendo el puerto: {exc}" + Style.RESET_ALL)


if __name__ == "__main__":
    escucha_puertos_main()
