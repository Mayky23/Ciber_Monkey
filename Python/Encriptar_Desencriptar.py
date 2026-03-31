from __future__ import annotations

import os
from pathlib import Path

from colorama import Back, Fore, Style, init
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from Python.ui import draw_banner, pause

init(autoreset=True)
COMMON_ASCII = r"""
 File Guardian
"""
BANNER_COLOR = "\033[95m"


def banner():
    draw_banner("", COMMON_ASCII, "Cifrar y descifrar archivos locales", BANNER_COLOR)


def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
        backend=default_backend(),
    )
    return kdf.derive(password)


def read_existing_path(prompt: str) -> Path:
    while True:
        path = Path(input(prompt).strip().strip('"')).expanduser()
        if path.exists() and path.is_file():
            return path
        print(Fore.BLACK + Back.RED + "Archivo no valido." + Style.RESET_ALL)


def read_output_directory() -> Path:
    while True:
        path = Path(input("Directorio de salida: ").strip().strip('"')).expanduser()
        if path.exists() and path.is_dir():
            return path
        print(Fore.BLACK + Back.RED + "Directorio no valido." + Style.RESET_ALL)


def read_password() -> bytes:
    password = input("Clave de cifrado/descifrado: ").strip()
    return password.encode("utf-8")


def encrypt_file(source: Path, password: bytes, output_dir: Path) -> Path:
    data = source.read_bytes()
    salt = os.urandom(16)
    iv = os.urandom(16)
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encrypted = cipher.encryptor().update(data)

    out_path = output_dir / f"{source.stem}.enc"
    out_path.write_bytes(salt + iv + encrypted)
    return out_path


def decrypt_file(source: Path, password: bytes, output_dir: Path) -> Path:
    payload = source.read_bytes()
    if len(payload) < 32:
        raise ValueError("El archivo cifrado es demasiado pequeno o no tiene formato valido.")
    salt, iv, encrypted = payload[:16], payload[16:32], payload[32:]
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decrypted = cipher.decryptor().update(encrypted)

    base_name = source.name[:-4] if source.name.endswith(".enc") else f"{source.name}.dec"
    out_path = output_dir / base_name
    out_path.write_bytes(decrypted)
    return out_path


def encriptar_desencriptar_main():
    while True:
        banner()
        print("\n1. Cifrar archivo")
        print("2. Descifrar archivo")
        print("n. Volver")
        option = input("\nSelecciona una opcion: ").strip().lower()

        if option == "n":
            return
        if option not in {"1", "2"}:
            pause(Fore.RED + "Opcion no valida. Pulsa Enter para continuar...")
            continue

        source = read_existing_path("Ruta del archivo: ")
        password = read_password()
        output_dir = read_output_directory()

        try:
            if option == "1":
                out_path = encrypt_file(source, password, output_dir)
                print(Fore.GREEN + f"Archivo cifrado correctamente: {out_path}")
            else:
                out_path = decrypt_file(source, password, output_dir)
                print(Fore.GREEN + f"Archivo descifrado correctamente: {out_path}")
        except Exception as exc:
            print(Fore.BLACK + Back.RED + f"Operacion fallida: {exc}" + Style.RESET_ALL)
        pause()


if __name__ == "__main__":
    encriptar_desencriptar_main()
