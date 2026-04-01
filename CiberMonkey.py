#!/usr/bin/env python3
"""Punto de entrada principal de Ciber Monkey."""

from __future__ import annotations

import importlib
import platform
import shutil
from dataclasses import dataclass
from typing import Callable, Iterable

from colorama import Back, Fore, Style, init

from Python.ui import clear_screen, draw_banner, pause

init(autoreset=True)

TITLE_ART = [
    (Fore.LIGHTCYAN_EX, r"   _______ __                 __  ___            __                                     "),
    (Fore.LIGHTCYAN_EX, r"  / ____(_) /_  ___  _____   /  |/  /___  ____  / /_____  __  __                        "),
    (Fore.CYAN,         r" / /   / / __ \/ _ \/ ___/  / /|_/ / __ \/ __ \/ //_/ _ \/ / / /                        "),
    (Fore.BLUE,         r"/ /___/ / /_/ /  __/ /     / /  / / /_/ / / / / ,< /  __/ /_/ /                         "),
    (Fore.MAGENTA,      r"\____/_/_.___/\___/_/     /_/  /_/\____/_/ /_/_/|_|\___/\__, /                          "),
    (Fore.LIGHTMAGENTA_EX, r"                                                       /____/                           "),
]
FRAME_COLOR = Fore.LIGHTCYAN_EX
ACCENT_COLOR = Fore.MAGENTA
PANEL_WIDTH = 64

@dataclass(frozen=True)
class MenuOption:
    key: int
    label: str
    action: Callable[[], object]

def print_ascii_art() -> None:
    clear_screen()
    for color, line in TITLE_ART:
        print(color + Style.BRIGHT + line + Style.RESET_ALL)
    print(ACCENT_COLOR + " " + "─" * (PANEL_WIDTH - 2))
    print(
        FRAME_COLOR
        + Style.BRIGHT
        + "  [By: Mayky]"
        + Style.RESET_ALL
        + Fore.WHITE
        + f"  Sistema: {platform.system()} {platform.release()}"
    )
    print(ACCENT_COLOR + " " + "─" * (PANEL_WIDTH - 2) + Style.RESET_ALL)


def print_menu(options: Iterable[MenuOption]) -> None:
    print(FRAME_COLOR + f"╔{'═' * PANEL_WIDTH}╗")
    print(FRAME_COLOR + "║" + Fore.WHITE + Style.BRIGHT + " MENU PRINCIPAL".ljust(PANEL_WIDTH) + FRAME_COLOR + "║")
    print(FRAME_COLOR + f"╠{'═' * PANEL_WIDTH}╣")
    for option in options:
        line = f" {option.key:>2}. {option.label}"
        print(FRAME_COLOR + "║" + Fore.CYAN + line.ljust(PANEL_WIDTH) + FRAME_COLOR + "║")
    print(FRAME_COLOR + f"╠{'═' * PANEL_WIDTH}╣")
    print(FRAME_COLOR + "║" + Fore.LIGHTCYAN_EX + " 98. Diagnostico del entorno".ljust(PANEL_WIDTH) + FRAME_COLOR + "║")
    print(FRAME_COLOR + "║" + Fore.LIGHTRED_EX + " 99. Salir del programa".ljust(PANEL_WIDTH) + FRAME_COLOR + "║")
    print(FRAME_COLOR + f"╚{'═' * PANEL_WIDTH}╝")
    print()
    print(
        ACCENT_COLOR
        + " Estado: "
        + Fore.GREEN
        + "READY"
    )


def get_menu_options() -> list[MenuOption]:
    return [
        MenuOption(1, "DB Audit", lazy_action("Python.Auditar_BD", "main")),
        MenuOption(2, "Calc CIDR", lazy_action("Python.Cal_CIDR", "calculate_cidr")),
        MenuOption(3, "Data Gen", lazy_action("Python.Data_generator", "data_generator_main")),
        MenuOption(4, "DDoS", lazy_action("Python.DDos_atack", "ddos_attack_main")),
        MenuOption(5, "File Guardian", lazy_action("Python.Encriptar_Desencriptar", "encriptar_desencriptar_main")),
        MenuOption(6, "Port Listener", lazy_action("Python.Escucha_ports", "escucha_puertos_main")),
        MenuOption(7, "Meta Spy", lazy_action("Python.Metadatos", "metadata_main")),
        MenuOption(8, "Pwd Generator", lazy_action("Python.Pswd_generator", "password_generator_main")),
        MenuOption(9, "SQL Injection", lazy_action("Python.SQL_injection", "sql_injection_main")),
        MenuOption(10, "Sub Finder", lazy_action("Python.Subdomain_Enum", "subdomain_enum_main")),
        MenuOption(11, "Wifi Scanner", lazy_action("Python.Wifi_Scanner", "wifi_scanner_main")),
    ]


def import_available(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        return True
    except Exception:
        return False


def lazy_action(module_name: str, function_name: str) -> Callable[[], object]:
    def runner() -> object:
        module = importlib.import_module(module_name)
        return getattr(module, function_name)()

    return runner


def run_doctor() -> None:
    print_ascii_art()
    essential_checks = [
        ("requests", import_available("requests")),
        ("cryptography", import_available("cryptography")),
        ("pymysql", import_available("pymysql")),
        ("dnspython", import_available("dns")),
        ("exifread", import_available("exifread")),
        ("scapy", import_available("scapy.all")),
        ("nmap", shutil.which("nmap") is not None),
        ("ping", shutil.which("ping") is not None),
        ("sqlmap", shutil.which("sqlmap") is not None),
    ]
    optional_checks = [
        ("pywifi", import_available("pywifi")),
        ("amass", shutil.which("amass") is not None),
        ("subfinder", shutil.which("subfinder") is not None),
        ("assetfinder", shutil.which("assetfinder") is not None),
        ("gobuster", shutil.which("gobuster") is not None),
        ("ffuf", shutil.which("ffuf") is not None),
    ]

    print(Fore.CYAN + "Revision rapida del entorno:\n" + Style.RESET_ALL)

    missing_essential = [name for name, ok in essential_checks if not ok]
    missing_optional = [name for name, ok in optional_checks if not ok]

    if not missing_essential:
        print(Fore.GREEN + "[OK] Base principal lista")
    else:
        print(Fore.RED + "[FALTA] Base principal: " + ", ".join(missing_essential))

    if missing_optional:
        print(Fore.YELLOW + "[OPCIONAL] Pendiente: " + ", ".join(missing_optional))
    else:
        print(Fore.GREEN + "[OK] Extras disponibles")

    print(Fore.WHITE + "\nUsa `install.sh` en Linux/Kali o `install.ps1` en Windows para completar lo que falte.")
    pause()


def salir() -> None:
    clear_screen()
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "Ciber Monkey" + Style.RESET_ALL)
    print(Fore.MAGENTA + "Sesion cerrada.\n" + Style.RESET_ALL)


def main() -> None:
    options = get_menu_options()
    options_by_key = {option.key: option.action for option in options}

    while True:
        print_ascii_art()
        print_menu(options)
        try:
            option = int(input("\nSelecciona una opcion: ").strip())
        except ValueError:
            print(Fore.BLACK + Back.RED + "Introduce un numero valido." + Style.RESET_ALL)
            pause()
            continue

        if option == 99:
            salir()
            break
        if option == 98:
            run_doctor()
            continue

        action = options_by_key.get(option)
        if action is None:
            print(Fore.BLACK + Back.RED + "Opcion no valida." + Style.RESET_ALL)
            pause()
            continue

        try:
            action()
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nOperacion cancelada por el usuario.")
            pause()
        except Exception as exc:
            print(Fore.BLACK + Back.RED + f"Se produjo un error: {exc}" + Style.RESET_ALL)
            pause()


if __name__ == "__main__":
    main()
