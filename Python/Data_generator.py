import random
import os

from colorama import Fore, Back, Style, init

# Inicializar colorama
init()

# Definir listas de datos para la generación de información personal
ALPHABET = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]

FIRST_NAMES = [
    "Juan", "María", "José", "Laura", "Carlos", "Sofía", "Luis", "Ana", "Pedro", "Marta",
    "Alejandro", "Isabella", "Diego", "Valentina", "Gabriel",
    "Fernando", "Adriana", "Miguel", "Elena", "Ricardo", "Beatriz", "Javier", "Claudia", "Raúl",
    "Natalia", "Roberto", "Monica", "Daniel", "Carolina", "Hugo", "Victoria", "Fabiola", "Eduardo",
    "Carmen", "Ángel", "Renata", "Pablo", "Lucía", "Raul", "Olivia", "Andrés", "Silvia", "Francisco"
]

LAST_NAMES = [
    "Gómez", "Rodríguez", "Fernández", "López", "Pérez", "González", "Martínez", "Sánchez", "Romero", "Torres",
    "Ortega", "Hernández", "Silva", "Ramírez", "Chavez", "Luna", "Mendoza", "Guerrero", "Cruz", "Vargas", 
    "Cabrera", "Cortez", "Román", "Castañeda", "Zapata", "Aguirre", "Moreno", "Delgado", "Ramos", "Orozco", 
    "Soto", "Molina", "Cisneros", "Fuentes", "Vega", "Giménez", "Rosales", "Flores", "Valdez", "Acosta", "Herrera", "Núñez", 
    "Carrillo", "Lara", "Escobar"
]

BANKS = [
    "Banco Santander", "BBVA", "CaixaBank", "Bankia", "Banco Sabadell",
    "Banco Popular", "ING Direct", "Bankinter", "Caja Rural",
    "Kutxabank", "Abanca", "Unicaja Banco", "Ibercaja", "Deutsche Bank",
    "Société Générale", "Barclays", "HSBC", "BNP Paribas", "Citibank"
]

EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
    "icloud.com", "mail.com", "live.com", "protonmail.com", "example.com"
]

# Función principal para la generación de datos personales.
def data_generator_main():
    while True:
        clear_screen()
        banner()
        response = input("¿Cuántas personas deseas generar? (Escribe 'n' para terminar)\n")

        if response.lower() == "n":
            break

        try:
            num_people = int(response)

            for i in range(num_people):
                print(f"Datos de la persona #{i + 1}")
                print("-----------------------------------------------------")
                dni = generate_dni()
                name, email = generate_name_and_email()
                bank_account = generate_bank_account()
                date_of_birth = generate_date_of_birth()
                password = generate_password()
                
                # Mostrar los datos generados de la persona.
                print("DNI:", dni)
                print("Nombre:", name)
                print("Email:", email)
                print("Cuenta bancaria:", bank_account)
                print("Fecha de nacimiento:", date_of_birth)
                print("Contraseña:", password)
                print("-----------------------------------------------------")

        except ValueError:
            print("Error: Ingresa un número válido o escribe 'n' para terminar.")

# Función para generar un DNI aleatorio.
def generate_dni():
    dni = ''.join(str(random.randint(0, 9)) for _ in range(8))
    return f"{dni}{random.choice(ALPHABET)}"

# Función para generar un nombre y un email aleatorios.
def generate_name_and_email():
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    domain = random.choice(EMAIL_DOMAINS)

    full_name = f"{first_name} {last_name}"
    
    # Generar un email utilizando la primera letra del nombre y el apellido completo
    email = f"{first_name.lower()[0]}{last_name.lower()}@{domain}"

    return full_name, email

# Función para generar una cuenta bancaria aleatoria.
def generate_bank_account():
    bank = random.choice(BANKS)
    account_number = ''.join(str(random.randint(0, 9)) for _ in range(10))
    return f"{bank} - {account_number}"

# Función para generar una fecha de nacimiento aleatoria.
def generate_date_of_birth():
    year = random.randint(1970, 2019)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year:04d}-{month:02d}-{day:02d}"

# Función para generar una contraseña aleatoria.
def generate_password():
    length = 8
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Función para mostrar el banner de la aplicación.
def banner():
    cartel = r"""
  ___       _           ___                       _           
 |   \ __ _| |_ __ _   / __|___ _ _  ___ _ _ __ _| |_ ___ _ _ 
 | |) / _` |  _/ _` | | (_ / -_) ' \/ -_) '_/ _` |  _/ _ \ '_|
 |___/\__,_|\__\__,_|  \___\___|_||_\___|_| \__,_|\__\___/_|  
                                                              
    """
    print(Fore.LIGHTYELLOW_EX + cartel)
    print("**************************************************************" + Style.RESET_ALL)

# Función para limpiar la pantalla de la consola.
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    clear_screen()
    banner()
    data_generator_main()