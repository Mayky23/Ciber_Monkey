# pip install cryptography

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def obtener_ruta_archivo():
    while True:
        ruta = input("Ingrese la ruta del archivo: ")
        if os.path.exists(ruta):
            return ruta
        else:
            print("La ruta especificada no existe. Inténtelo de nuevo.")

def obtener_clave():
    clave = input("Ingrese la clave de encriptación/desencriptación: ")
    return clave.encode()

def encriptar_archivo(ruta, clave):
    with open(ruta, "rb") as archivo:
        datos = archivo.read()

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=algorithms.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    clave_derivada = kdf.derive(clave)

    cipher = Cipher(algorithms.AES(clave_derivada), modes.CFB(salt), backend=default_backend())
    encryptor = cipher.encryptor()
    datos_encriptados = encryptor.update(datos) + encryptor.finalize()

    with open("encriptado_" + os.path.basename(ruta), "wb") as archivo_encriptado:
        archivo_encriptado.write(salt + datos_encriptados)

    print("Archivo encriptado exitosamente.")

def desencriptar_archivo(ruta, clave):
    with open(ruta, "rb") as archivo_encriptado:
        datos_encriptados = archivo_encriptado.read()

    salt = datos_encriptados[:16]
    datos_encriptados = datos_encriptados[16:]

    kdf = PBKDF2HMAC(
        algorithm=algorithms.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    clave_derivada = kdf.derive(clave)

    cipher = Cipher(algorithms.AES(clave_derivada), modes.CFB(salt), backend=default_backend())
    decryptor = cipher.decryptor()
    datos_desencriptados = decryptor.update(datos_encriptados) + decryptor.finalize()

    with open("desencriptado_" + os.path.basename(ruta), "wb") as archivo_desencriptado:
        archivo_desencriptado.write(datos_desencriptados)

    print("Archivo desencriptado exitosamente.")

def encriptar_desencriptar_main():
    opcion = input("¿Desea encriptar (escriba 1) o desencriptar (escriba 2)?: ")

    if opcion == "1":
        ruta_archivo = obtener_ruta_archivo()
        clave = obtener_clave()
        encriptar_archivo(ruta_archivo, clave)

    elif opcion == "2":
        ruta_archivo = obtener_ruta_archivo()
        clave = obtener_clave()
        desencriptar_archivo(ruta_archivo, clave)

    else:
        print("Opción no válida.")

if __name__ == "__main__":
    encriptar_desencriptar_main()
