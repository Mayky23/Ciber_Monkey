from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from colorama import Fore, init
from Python.ui import draw_banner, pause, print_error, print_info, print_ok

init(autoreset=True)

TOOLS = ("gobuster", "ffuf")
COMMON_ASCII = r"""
 Sub Finder
"""
BANNER_COLOR = "\033[36m"


def banner():
    draw_banner("", COMMON_ASCII, "gobuster / ffuf", BANNER_COLOR)


def available_tools() -> list[str]:
    return [tool for tool in TOOLS if shutil.which(tool)]


def normalize_domain(value: str) -> str:
    raw = value.strip().lower()
    if not raw:
        return ""
    if "://" in raw:
        raw = urlparse(raw).hostname or ""
    raw = raw.strip().strip("/")
    if raw.startswith("www."):
        raw = raw[4:]
    return raw


def run_command(command: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout


def parse_gobuster_output(output: str, domain: str) -> set[str]:
    results = set()
    for line in output.splitlines():
        value = line.strip()
        if not value:
            continue
        token = value.split()[0].strip()
        token = token.replace("Found:", "").strip()
        token = token.replace("http://", "").replace("https://", "").strip("/")
        if token == domain or token.endswith(f".{domain}"):
            results.add(token)
    return results


def parse_ffuf_output(output: str, domain: str) -> set[str]:
    results = set()
    for line in output.splitlines():
        value = line.strip()
        if not value:
            continue
        if value.startswith(("::", "#", "[", " /'___", " |", " \\___")):
            continue
        token = value.split()[0].strip().strip(".")
        if token and " " not in token:
            results.add(f"{token}.{domain}")
    return results


def enum_with_gobuster(target_url: str, domain: str, wordlist: str) -> set[str]:
    command = [
        "gobuster",
        "vhost",
        "-u",
        target_url,
        "-w",
        wordlist,
        "-q",
        "-k",
        "--append-domain",
    ]
    code, output = run_command(command)
    if code not in {0, 1}:
        raise RuntimeError("gobuster no pudo completarse.")
    return parse_gobuster_output(output, domain)


def enum_with_ffuf(target_url: str, domain: str, wordlist: str) -> set[str]:
    command = [
        "ffuf",
        "-u",
        target_url,
        "-H",
        f"Host: FUZZ.{domain}",
        "-w",
        wordlist,
        "-mc",
        "all",
        "-fs",
        "0",
        "-c",
    ]
    code, output = run_command(command)
    if code not in {0, 1}:
        raise RuntimeError("ffuf no pudo completarse.")
    return parse_ffuf_output(output, domain)


def save_results(path: Path, values: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(values) + ("\n" if values else ""), encoding="utf-8")


def subdomain_enum_main():
    while True:
        banner()
        tools = available_tools()
        if not tools:
            print_error("No se encontro ninguna herramienta compatible (`gobuster`, `ffuf`).")
            pause("Instalala en Kali o anadela al PATH. Pulsa Enter para volver...")
            return

        print_info("Herramientas detectadas: " + ", ".join(tools))
        domain_input = input("Dominio o URL objetivo ('n' para volver): ").strip().lower()
        if domain_input == "n":
            return

        domain = normalize_domain(domain_input)
        if not domain or " " in domain:
            pause(Fore.RED + "Dominio no valido. Pulsa Enter para continuar...")
            continue

        scheme = input("Esquema base [http/https] (default http): ").strip().lower() or "http"
        if scheme not in {"http", "https"}:
            pause(Fore.RED + "Esquema no valido. Pulsa Enter para continuar...")
            continue

        target_url = f"{scheme}://{domain}"
        wordlist = input("Wordlist [ /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt ]: ").strip()
        if not wordlist:
            wordlist = "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
        if not Path(wordlist).exists():
            pause(Fore.RED + f"No existe la wordlist: {wordlist}")
            continue

        output = input("Archivo de salida [subdominios.txt]: ").strip() or "subdominios.txt"
        all_results: set[str] = set()

        for tool in tools:
            print_info(f"[*] Ejecutando {tool}...")
            try:
                if tool == "gobuster":
                    all_results.update(enum_with_gobuster(target_url, domain, wordlist))
                elif tool == "ffuf":
                    all_results.update(enum_with_ffuf(target_url, domain, wordlist))
            except Exception as exc:
                print(Fore.RED + f"[!] {tool} fallo: {exc}")

        filtered = sorted(value for value in all_results if value == domain or value.endswith(f".{domain}"))
        save_results(Path(output), filtered)

        print_ok(f"\nSubdominios encontrados: {len(filtered)}")
        for item in filtered:
            print(item)
        print(Fore.YELLOW + f"\nResultados guardados en: {Path(output).resolve()}")
        pause()


if __name__ == "__main__":
    subdomain_enum_main()
