from __future__ import annotations

import os

from colorama import Back, Fore, Style, init

init(autoreset=True)

COMMON_ASCII = r"""
     ___  ___   ___                      _   
    |   \| _ ) |_ _|_ _  ____ __  ___ __| |_ 
    | |) | _ \  | || ' \(_-< '_ \/ -_) _|  _|
    |___/|___/ |___|_||_/__/ .__/\___\__|\__|
                           |_|            
"""


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def draw_banner(
    title: str,
    ascii_art: str = "",
    subtitle: str | None = None,
    banner_color: str = Fore.LIGHTCYAN_EX,
) -> None:
    clear_screen()
    banner_art = ascii_art.strip("\n") if ascii_art else COMMON_ASCII.strip("\n")
    print(banner_color + Style.BRIGHT + banner_art + Style.RESET_ALL)
    print(banner_color + "─" * 58)
    if title:
        print(Fore.WHITE + f" {title}")
    if subtitle:
        print(banner_color + f" {subtitle}")
    print(banner_color + "─" * 58 + Style.RESET_ALL)


def pause(message: str = "Pulsa Enter para continuar...") -> None:
    input(Style.RESET_ALL + message)


def print_error(message: str) -> None:
    print(Fore.BLACK + Back.RED + message + Style.RESET_ALL)


def print_ok(message: str) -> None:
    print(Fore.GREEN + message + Style.RESET_ALL)


def print_info(message: str) -> None:
    print(Fore.CYAN + message + Style.RESET_ALL)
