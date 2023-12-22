import random

ALPHABET = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]

FIRST_NAMES = [
    "Juan", "María", "José", "Laura", "Carlos", "Sofía", "Luis", "Ana", "Pedro", "Marta",
    "Alejandro", "Isabella", "Diego", "Valentina", "Gabriel"
]

LAST_NAMES = [
    "Gómez", "Rodríguez", "Fernández", "López", "Pérez", "González", "Martínez", "Sánchez", "Romero", "Torres",
    "Ortega", "Hernández", "Silva", "Ramírez", "Chavez"
]

EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
    "icloud.com", "mail.com", "live.com", "protonmail.com", "example.com"
]

BANKS = [
    "Banco A", "Banco B", "Banco C", "Banco D", "Banco E",
    "Banco F", "Banco G", "Banco H", "Banco I", "Banco J"
]


def data_generator_main():
    while True:
        response = input("¿Cuántas personas deseas generar? (Escribe 'salir' para terminar)\n")

        if response.lower() == "salir":
            break

        try:
            num_people = int(response)

            for i in range(num_people):
                print(f"Datos de la persona #{i + 1}")
                print("-----------------------------------------------------")
                print("DNI:", generate_dni())
                print("Nombre:", generate_name())
                print("Email:", generate_email())
                print("Cuenta bancaria:", generate_bank_account())
                print("Fecha de nacimiento:", generate_date_of_birth())
                print("Contraseña:", generate_password())
                print("-----------------------------------------------------")

        except ValueError:
            print("Error: Ingresa un número válido o escribe 'salir' para terminar.")


def generate_dni():
    dni = ''.join(str(random.randint(0, 9)) for _ in range(8))
    return f"{dni}{random.choice(ALPHABET)}"


def generate_name():
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return f"{first_name} {last_name}"


def generate_email():
    first_name = random.choice(FIRST_NAMES).lower()
    last_name = random.choice(LAST_NAMES).lower()
    domain = random.choice(EMAIL_DOMAINS)
    variation = random.choice([".", "_", ""])
    email = f"{first_name}{variation}{last_name}@{domain}"
    return email


def generate_bank_account():
    bank = random.choice(BANKS)
    account_number = ''.join(str(random.randint(0, 9)) for _ in range(10))
    return f"{bank} - {account_number}"


def generate_date_of_birth():
    year = random.randint(1970, 2019)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year:04d}-{month:02d}-{day:02d}"


def generate_password():
    length = 8
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


if __name__ == "__main__":
    data_generator_main()
