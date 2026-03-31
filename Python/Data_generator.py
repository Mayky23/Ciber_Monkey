import random
from colorama import Fore, Style, init
from Python.ui import draw_banner, pause

init(autoreset=True)
COMMON_ASCII = r"""
 Data Gen
"""
BANNER_COLOR = "\033[92m"

ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
FIRST_NAMES = [
    "Juan", "Maria", "Jose", "Laura", "Carlos", "Sofia", "Luis", "Ana",
    "Pedro", "Marta", "Alejandro", "Isabella", "Diego", "Valentina",
    "Gabriel", "Fernando", "Adriana", "Miguel", "Elena", "Ricardo",
    "Beatriz", "Javier", "Claudia", "Raul", "Natalia", "Roberto",
    "Monica", "Daniel", "Carolina", "Hugo", "Victoria", "Fabiola",
    "Eduardo", "Carmen", "Angel", "Renata", "Pablo", "Lucia",
    "Olivia", "Andres", "Silvia", "Francisco",
]
LAST_NAMES = [
    "Gomez", "Rodriguez", "Fernandez", "Lopez", "Perez", "Gonzalez",
    "Martinez", "Sanchez", "Romero", "Torres", "Ortega", "Hernandez",
    "Silva", "Ramirez", "Chavez", "Luna", "Mendoza", "Guerrero", "Cruz",
    "Vargas", "Cabrera", "Cortez", "Roman", "Castaneda", "Zapata",
    "Aguirre", "Moreno", "Delgado", "Ramos", "Orozco", "Soto", "Molina",
    "Cisneros", "Fuentes", "Vega", "Gimenez", "Rosales", "Flores",
    "Valdez", "Acosta", "Herrera", "Nunez", "Carrillo", "Lara", "Escobar",
]
BANKS = [
    "Banco Santander", "BBVA", "CaixaBank", "Banco Sabadell", "Bankinter",
    "Kutxabank", "Abanca", "Unicaja Banco", "Ibercaja", "Deutsche Bank",
    "Barclays", "HSBC", "BNP Paribas", "Citibank",
]
EMAIL_DOMAINS = [
    "gmail.com", "outlook.com", "hotmail.com", "protonmail.com", "example.com",
]
def banner():
    draw_banner("", COMMON_ASCII, "Datos ficticios para pruebas", BANNER_COLOR)


def generate_dni():
    base = "".join(str(random.randint(0, 9)) for _ in range(8))
    return f"{base}{random.choice(ALPHABET)}"


def generate_name_and_email():
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    domain = random.choice(EMAIL_DOMAINS)
    alias = f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}"
    return f"{first_name} {last_name}", f"{alias}@{domain}"


def generate_bank_account():
    iban_body = "".join(str(random.randint(0, 9)) for _ in range(20))
    bank = random.choice(BANKS)
    return f"{bank} - ES{random.randint(10, 99)} {iban_body[:4]} {iban_body[4:8]} {iban_body[8:12]} {iban_body[12:16]} {iban_body[16:]}"


def generate_date_of_birth():
    year = random.randint(1970, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year:04d}-{month:02d}-{day:02d}"


def generate_password():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"
    return "".join(random.choice(chars) for _ in range(12))


def data_generator_main():
    while True:
        banner()
        response = input("Cuantas identidades ficticias deseas generar? ('n' para volver): ").strip()
        if response.lower() == "n":
            return
        try:
            num_people = int(response)
            if num_people <= 0:
                raise ValueError
        except ValueError:
            pause(Fore.RED + "Introduce un numero entero positivo. Pulsa Enter para continuar...")
            continue

        banner()
        for i in range(1, num_people + 1):
            name, email = generate_name_and_email()
            print(Fore.CYAN + f"Persona #{i}")
            print("-" * 60)
            print("DNI:", generate_dni())
            print("Nombre:", name)
            print("Email:", email)
            print("Cuenta bancaria:", generate_bank_account())
            print("Fecha de nacimiento:", generate_date_of_birth())
            print("Password:", generate_password())
            print("-" * 60)
        pause()


if __name__ == "__main__":
    data_generator_main()
