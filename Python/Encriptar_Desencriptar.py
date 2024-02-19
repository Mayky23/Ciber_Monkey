from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from colorama import Fore, Back, Style

def obtener_ruta_archivo():
    while True:
        ruta = input("Ingrese la ruta del archivo: ")
        if os.path.exists(ruta):
            return ruta
        else:
            print(Fore.BLACK + Back.RED + "La ruta especificada no existe. Inténtelo de nuevo." + Style.RESET_ALL)

def obtener_clave():
    clave = input("Ingrese la clave de encriptación/desencriptación: ")
    return clave.encode()

def encriptar_archivo(ruta, clave):
    with open(ruta, "rb") as archivo:
        datos = archivo.read()

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    clave_derivada = kdf.derive(clave)

    cipher = Cipher(algorithms.AES(clave_derivada), modes.CFB(salt), backend=default_backend())
    encryptor = cipher.encryptor()
    datos_encriptados = encryptor.update(datos) + encryptor.finalize()

    with open("encriptado_" + os.path.basename(ruta), "wb") as archivo_encriptado:
        archivo_encriptado.write(salt + datos_encriptados)

    print(Fore.BLACK + Back.GREEN + "Archivo encriptado exitosamente." + Style.RESET_ALL)

def desencriptar_archivo(ruta, clave):
    with open(ruta, "rb") as archivo_encriptado:
        datos_encriptados = archivo_encriptado.read()

    salt = datos_encriptados[:16]
    datos_encriptados = datos_encriptados[16:]

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    clave_derivada = kdf.derive(clave)

    cipher = Cipher(algorithms.AES(clave_derivada), modes.CFB(salt), backend=default_backend())
    decryptor = cipher.decryptor()
    datos_desencriptados = decryptor.update(datos_encriptados) + decryptor.finalize()

    with open("desencriptado_" + os.path.basename(ruta), "wb") as archivo_desencriptado:
        archivo_desencriptado.write(datos_desencriptados)

    print(Fore.BLACK + Back.GREEN + "Archivo desencriptado exitosamente." + Style.RESET_ALL)

def encriptar_desencriptar_main():
    opcion = input(Style.RESET_ALL + "¿Desea encriptar (1) o desencriptar (2)?: ")

    if opcion == "1":
        ruta_archivo = obtener_ruta_archivo()
        clave = obtener_clave()
        encriptar_archivo(ruta_archivo, clave)

    elif opcion == "2":
        ruta_archivo = obtener_ruta_archivo()
        clave = obtener_clave()
        desencriptar_archivo(ruta_archivo, clave)

    else:
        print(Fore.BLACK + Back.RED + "Opción no válida." + Style.RESET_ALL)

def mostrar_menu():
    banner()
    print("************************")
    print("*         FILE         *")
    print("************************")
    print("*    1. Encriptar      *")
    print("*    2. Desencriptar   *")
    print("************************")

def banner():
    cartel = r"""
   ___ _ _        ___                  _ _           
  | __(_) |___   / __|_  _ __ _ _ _ __| (_)__ _ _ _  
  | _|| | / -_) | (_ | || / _` | '_/ _` | / _` | ' \ 
  |_| |_|_\___|  \___|\_,_\__,_|_| \__,_|_\__,_|_||_|
    """
    print(Fore.WHITE + cartel)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    clear_screen()
    mostrar_menu()
    encriptar_desencriptar_main()
