from __future__ import annotations

import ipaddress

from colorama import Back, Fore, Style, init
from Python.ui import draw_banner, pause

init(autoreset=True)
COMMON_ASCII = r"""
 Calc CIDR
"""
BANNER_COLOR = "\033[94m"

def banner():
    draw_banner("", COMMON_ASCII, "IPv4 / IPv6", BANNER_COLOR)


def calculate_cidr():
    while True:
        banner()
        value = input("Introduce IP/CIDR ('n' para volver): ").strip()
        if value.lower() == "n":
            return

        try:
            network = ipaddress.ip_network(value, strict=False)
        except ValueError as exc:
            pause(Fore.BLACK + Back.RED + f"Entrada invalida: {exc}" + Style.RESET_ALL)
            continue

        print(Fore.CYAN + f"Red: {network}")
        print(f"Version IP: IPv{network.version}")
        print(f"Direccion de red: {network.network_address}")
        if network.version == 4:
            print(f"Broadcast: {network.broadcast_address}")
        print(f"Prefijo: /{network.prefixlen}")
        print(f"Mascara: {getattr(network, 'netmask', 'N/A')}")
        print(f"Hosts totales: {network.num_addresses}")

        hosts = list(network.hosts())
        if hosts:
            print(f"Primer host: {hosts[0]}")
            print(f"Ultimo host: {hosts[-1]}")
        else:
            print("No hay hosts utilizables en esta red.")
        pause()
