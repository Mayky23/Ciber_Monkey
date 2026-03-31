import secrets

from colorama import Back, Fore, Style, init
from Python.ui import draw_banner, pause

init(autoreset=True)
COMMON_ASCII = r"""
 Pwd Generator
"""
BANNER_COLOR = "\033[97m"

CARACTERES_MINUSCULAS = "abcdefghijklmnopqrstuvwxyz"
CARACTERES_MAYUSCULAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMEROS = "0123456789"
CARACTERES_ESPECIALES = "!@#$%^&*()_+-=[]{}|;:,.?/"


def generar_contrasena(longitud, opciones):
    alphabet = ""
    if "min" in opciones:
        alphabet += CARACTERES_MINUSCULAS
    if "may" in opciones:
        alphabet += CARACTERES_MAYUSCULAS
    if "num" in opciones:
        alphabet += NUMEROS
    if "espc" in opciones:
        alphabet += CARACTERES_ESPECIALES
    if not alphabet:
        raise ValueError("Debes seleccionar al menos un grupo de caracteres.")
    return "".join(secrets.choice(alphabet) for _ in range(longitud))


def password_generator_main():
    while True:
        banner()
        answer = input("Generar una contrasena? (s/n): ").strip().lower()
        if answer == "n":
            return
        if answer != "s":
            pause(Fore.RED + "Opcion no valida. Pulsa Enter para continuar...")
            continue

        try:
            longitud = int(input("Longitud deseada: ").strip())
            if longitud <= 0:
                raise ValueError
        except ValueError:
            pause(Fore.BLACK + Back.RED + "Longitud invalida." + Style.RESET_ALL)
            continue

        opciones = input("Grupos a usar (min/may/num/espc): ").strip().lower().split("/")
        if not all(opcion in {"min", "may", "num", "espc"} for opcion in opciones):
            pause(Fore.BLACK + Back.RED + "Opciones invalidas." + Style.RESET_ALL)
            continue

        try:
            password = generar_contrasena(longitud, opciones)
        except ValueError as exc:
            pause(Fore.BLACK + Back.RED + str(exc) + Style.RESET_ALL)
            continue

        print(Fore.LIGHTYELLOW_EX + "\nContrasena generada:")
        print(Style.RESET_ALL + password)
        pause()


def banner():
    draw_banner("", COMMON_ASCII, "Longitud y grupos personalizables", BANNER_COLOR)


if __name__ == "__main__":
    password_generator_main()
