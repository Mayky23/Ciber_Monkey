from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from colorama import Fore, init

from Python.ui import draw_banner, pause, print_error, print_info, print_ok

init(autoreset=True)
COMMON_ASCII = r"""
 Escaneo de directorios web
"""
BANNER_COLOR = "\033[35m"


def banner():
    draw_banner("", COMMON_ASCII, "gobuster / ffuf", BANNER_COLOR)


def available_tools() -> list[str]:
    tools = []
    if shutil.which("gobuster"):
        tools.append("gobuster")
    if shutil.which("ffuf"):
        tools.append("ffuf")
    return tools


def run_gobuster(url: str, wordlist: str, extensions: str, output: Path) -> None:
    command = ["gobuster", "dir", "-u", url, "-w", wordlist, "-q", "-k", "-o", str(output)]
    if extensions.strip():
        command.extend(["-x", extensions])
    subprocess.run(command, check=False)


def run_ffuf(url: str, wordlist: str, output: Path) -> None:
    base_url = url.rstrip("/") + "/FUZZ"
    command = ["ffuf", "-u", base_url, "-w", wordlist, "-fc", "404", "-of", "json", "-o", str(output)]
    subprocess.run(command, check=False)


def web_directory_scan_main():
    while True:
        banner()
        tools = available_tools()
        if not tools:
            print_error("No se encontro `gobuster` ni `ffuf` en PATH.")
            pause("Instalalos en Kali para usar esta opcion. Pulsa Enter para volver...")
            return

        print_info("Herramientas detectadas: " + ", ".join(tools))
        url = input("URL objetivo ('n' para volver): ").strip()
        if url.lower() == "n":
            return
        if not url.startswith(("http://", "https://")):
            pause(Fore.RED + "La URL debe empezar por http:// o https://")
            continue

        wordlist = input("Wordlist [ /usr/share/wordlists/dirb/common.txt ]: ").strip()
        if not wordlist:
            wordlist = "/usr/share/wordlists/dirb/common.txt"
        if not Path(wordlist).exists():
            pause(Fore.RED + f"No existe la wordlist: {wordlist}")
            continue

        extensions = input("Extensiones para gobuster (ej: php,txt,html) [vacio=ninguna]: ").strip()
        output_dir = Path(input("Directorio de salida [web_scan_results]: ").strip() or "web_scan_results")
        output_dir.mkdir(parents=True, exist_ok=True)

        if "gobuster" in tools:
            gobuster_output = output_dir / "gobuster.txt"
            print_info(f"[*] Ejecutando gobuster -> {gobuster_output}")
            run_gobuster(url, wordlist, extensions, gobuster_output)

        if "ffuf" in tools:
            ffuf_output = output_dir / "ffuf.json"
            print_info(f"[*] Ejecutando ffuf -> {ffuf_output}")
            run_ffuf(url, wordlist, ffuf_output)

        print_ok(f"Escaneo completado. Revisa los resultados en: {output_dir.resolve()}")
        pause()
