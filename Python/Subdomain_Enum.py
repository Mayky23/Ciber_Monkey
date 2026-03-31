from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from colorama import Back, Fore, Style, init
from Python.ui import draw_banner, pause, print_error, print_info, print_ok

init(autoreset=True)

TOOLS = ("amass", "subfinder", "assetfinder")
COMMON_ASCII = r"""
 Sub Finder
"""
BANNER_COLOR = "\033[36m"
def banner():
    draw_banner("", COMMON_ASCII, "amass / subfinder / assetfinder", BANNER_COLOR)


def available_tools() -> list[str]:
    return [tool for tool in TOOLS if shutil.which(tool)]


def run_command(command: list[str]) -> set[str]:
    proc = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    results = set()
    for line in proc.stdout.splitlines():
        value = line.strip()
        if value:
            results.add(value)
    return results


def enum_with_tool(tool: str, domain: str) -> set[str]:
    if tool == "amass":
        return run_command(["amass", "enum", "-passive", "-norecursive", "-d", domain])
    if tool == "subfinder":
        return run_command(["subfinder", "-silent", "-d", domain])
    if tool == "assetfinder":
        return {value for value in run_command(["assetfinder", "--subs-only", domain]) if value.endswith(domain)}
    return set()


def save_results(path: Path, values: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(values) + ("\n" if values else ""), encoding="utf-8")


def subdomain_enum_main():
    while True:
        banner()
        tools = available_tools()
        if not tools:
            print_error("No se encontro ninguna herramienta compatible (`amass`, `subfinder`, `assetfinder`).")
            pause("Instalala en Kali o anadela al PATH. Pulsa Enter para volver...")
            return

        print_info("Herramientas detectadas: " + ", ".join(tools))
        domain = input("Dominio objetivo ('n' para volver): ").strip().lower()
        if domain == "n":
            return
        if not domain or " " in domain or "://" in domain:
            pause(Fore.RED + "Dominio no valido. Pulsa Enter para continuar...")
            continue

        output = input("Archivo de salida [subdominios.txt]: ").strip() or "subdominios.txt"
        all_results: set[str] = set()

        for tool in tools:
            print_info(f"[*] Ejecutando {tool}...")
            try:
                all_results.update(enum_with_tool(tool, domain))
            except Exception as exc:
                print(Fore.RED + f"[!] {tool} fallo: {exc}")

        filtered = sorted(value for value in all_results if value == domain or value.endswith(f".{domain}"))
        save_results(Path(output), filtered)

        print_ok(f"\nSubdominios encontrados: {len(filtered)}")
        for item in filtered:
            print(item)
        print(Fore.YELLOW + f"\nResultados guardados en: {Path(output).resolve()}")
        pause()
