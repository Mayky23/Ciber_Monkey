"""Wrapper para sqlmap en entornos autorizados."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from colorama import Back, Fore, Style, init
from Python.ui import draw_banner, pause, print_error, print_info, print_ok

init(autoreset=True)
COMMON_ASCII = r"""
 SQL Injection
"""
BANNER_COLOR = "\033[31m"

def banner():
    draw_banner("", COMMON_ASCII, "Wrapper guiado para sqlmap", BANNER_COLOR)


def build_sqlmap_command(
    target_url: str,
    output_dir: str,
    level: str,
    risk: str,
    extra_args: str,
    use_forms: bool,
) -> list[str]:
    command = [
        "sqlmap",
        "-u",
        target_url,
        "--batch",
        "--random-agent",
        "--level",
        level,
        "--risk",
        risk,
        "--output-dir",
        output_dir,
    ]
    if use_forms:
        command.append("--forms")
    if extra_args.strip():
        command.extend(extra_args.split())
    return command


def run_sqlmap(command: list[str]) -> int:
    process = subprocess.Popen(command)
    return process.wait()


def sql_injection_main():
    while True:
        banner()
        if not shutil.which("sqlmap"):
            print_error("No se encontro `sqlmap` en PATH. Instala sqlmap en Kali o anadelo al sistema.")
            pause()
            return

        print("1. URL con parametro GET")
        print("2. Formulario web")
        print("\nEjemplos del lab:")
        print("- GET:  http://IP_DEL_HOST:8081/api/products?id=1")
        print("- FORM: http://IP_DEL_HOST:8081/site/index.html  (o la URL del frontend con formulario)")
        mode = input("\nModo [1/2] ('n' para volver): ").strip().lower()
        if mode == "n":
            return
        if mode not in {"1", "2"}:
            pause(Fore.RED + "Modo no valido. Pulsa Enter...")
            continue

        target_url = input("URL objetivo ('n' para volver): ").strip()
        if target_url.lower() == "n":
            return
        if not target_url.startswith(("http://", "https://")):
            pause(Fore.RED + "La URL debe empezar por http:// o https://. Pulsa Enter...")
            continue

        level = input("Nivel sqlmap [1-5] (default 2): ").strip() or "2"
        risk = input("Riesgo sqlmap [1-3] (default 1): ").strip() or "1"
        output_dir = input("Directorio de salida [sqlmap_output]: ").strip() or "sqlmap_output"
        extra_args = input(
            "Argumentos extra opcionales (ej: --cookie=PHPSESSID=... --dbs), vacio si no hace falta: "
        )

        use_forms = mode == "2"
        command = build_sqlmap_command(target_url, output_dir, level, risk, extra_args, use_forms)
        print_info("\nComando a ejecutar:")
        print(" ".join(command))
        confirm = input("\nEjecutar sqlmap? (s/n): ").strip().lower()
        if confirm != "s":
            continue

        code = run_sqlmap(command)
        resolved_output = Path(output_dir).resolve()
        if code == 0:
            print_ok(f"\nsqlmap finalizo correctamente. Revisa: {resolved_output}")
        else:
            print(Fore.YELLOW + f"\nsqlmap termino con codigo {code}. Revisa: {resolved_output}")
        pause()


if __name__ == "__main__":
    sql_injection_main()
