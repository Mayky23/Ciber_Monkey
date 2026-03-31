"""Pruebas de disponibilidad de servicios autorizados.

Mantiene la compatibilidad con el nombre historico del modulo, pero ya no
implementa un flood continuo.
"""

from __future__ import annotations

import socket
import time
from contextlib import closing

from colorama import Fore, init
from Python.ui import draw_banner, pause

init(autoreset=True)
COMMON_ASCII = r"""
 DDoS
"""
BANNER_COLOR = "\033[91m"


def banner():
    draw_banner("", COMMON_ASCII, "Prueba controlada de latencia", BANNER_COLOR)


def resolve_target(target: str) -> str:
    return socket.gethostbyname(target)


def probe_tcp(ip: str, port: int, attempts: int, timeout: float) -> list[float]:
    timings = []
    for _ in range(attempts):
        start = time.perf_counter()
        try:
            with closing(socket.create_connection((ip, port), timeout=timeout)):
                elapsed = (time.perf_counter() - start) * 1000
                timings.append(elapsed)
        except OSError:
            elapsed = (time.perf_counter() - start) * 1000
            timings.append(elapsed)
        time.sleep(0.2)
    return timings


def ddos_attack_main():
    while True:
        banner()
        print("Uso autorizado y defensivo solamente.\n")
        target = input("Host o IP a comprobar ('n' para volver): ").strip()
        if target.lower() == "n":
            return

        try:
            ip = resolve_target(target)
        except socket.gaierror:
            pause(Fore.RED + "No se pudo resolver el objetivo. Pulsa Enter para continuar...")
            continue

        try:
            port = int(input("Puerto TCP a comprobar: ").strip())
            attempts = int(input("Numero de intentos (1-20, recomendado 5): ").strip() or "5")
        except ValueError:
            pause(Fore.RED + "Debes introducir numeros validos. Pulsa Enter para continuar...")
            continue

        attempts = max(1, min(20, attempts))
        timings = probe_tcp(ip, port, attempts=attempts, timeout=2.0)
        avg = sum(timings) / len(timings)

        print(Fore.CYAN + f"\nObjetivo resuelto: {target} -> {ip}")
        print("Tiempos por intento (ms):", ", ".join(f"{t:.2f}" for t in timings))
        print(Fore.GREEN + f"Latencia media: {avg:.2f} ms")
        print(
            Fore.YELLOW
            + "Si el servicio no responde, revisa firewall, routing o que el puerto este escuchando."
        )
        pause()


if __name__ == "__main__":
    ddos_attack_main()
