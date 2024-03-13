# Importación de módulos necesarios de la biblioteca cryptography para la generación de claves y cifrado.
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# Importación del módulo 'os' para manipulación de archivos y del módulo 'colorama' para mejorar la presentación en consola.
import os
from colorama import Fore, Back, Style

# Definición de la función para obtener la ruta donde se guardará el archivo encriptado/desencriptado.
def obtener_ruta_guardado():
    while True:
        ruta = input("Ingrese la ruta donde se guardará el archivo encriptado/desencriptado: ")
        # Verifica si la ruta especificada es un directorio válido.
        if os.path.isdir(os.path.dirname(ruta)):
            return ruta
        else:
            # Informa al usuario que la ruta especificada no es válida.
            print(Fore.BLACK + Back.RED + "La ruta especificada no es válida. Inténtelo de nuevo." + Style.RESET_ALL)

# Definición de la función para obtener la ruta del archivo a encriptar/desencriptar.
def obtener_ruta_archivo():
    while True:
        ruta = input("Ingrese la ruta del archivo: ")
        # Verifica si la ruta especificada existe.
        if os.path.exists(ruta):
            return ruta
        else:
            # Informa al usuario que la ruta especificada no existe.
            print(Fore.BLACK + Back.RED + "La ruta especificada no existe. Inténtelo de nuevo." + Style.RESET_ALL)

# Definición de la función para obtener la clave de encriptación/desencriptación.
def obtener_clave():
    clave = input("Ingrese la clave de encriptación/desencriptación: ")
    return clave.encode()

# Definición de la función para encriptar un archivo.
def encriptar_archivo(ruta, clave, ruta_guardado):
    with open(ruta, "rb") as archivo:
        datos = archivo.read()

    # Generación de un valor aleatorio como sal para el algoritmo PBKDF2.
    salt = os.urandom(16)
    # Creación de un objeto PBKDF2HMAC para derivar una clave a partir de la clave ingresada.
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    clave_derivada = kdf.derive(clave)

    # Creación de un objeto Cipher para cifrar los datos usando AES en modo CFB.
    cipher = Cipher(algorithms.AES(clave_derivada), modes.CFB(salt), backend=default_backend())
    encryptor = cipher.encryptor()
    datos_encriptados = encryptor.update(datos) + encryptor.finalize()

    # Nombre del archivo encriptado.
    nombre_archivo = "encriptado_" + os.path.basename(ruta)
    ruta_archivo_encriptado = os.path.join(ruta_guardado, nombre_archivo)

    # Escritura de los datos encriptados en un nuevo archivo.
    with open(ruta_archivo_encriptado, "wb") as archivo_encriptado:
        archivo_encriptado.write(salt + datos_encriptados)

    # Informa al usuario que el archivo ha sido encriptado y guardado exitosamente.
    print(Fore.BLACK + Back.GREEN + "Archivo encriptado y guardado en {} exitosamente.".format(ruta_archivo_encriptado) + Style.RESET_ALL)

# Definición de la función para desencriptar un archivo.
def desencriptar_archivo(ruta, clave, ruta_guardado):
    with open(ruta, "rb") as archivo_encriptado:
        datos_encriptados = archivo_encriptado.read()

    # Extrae el valor del salt del inicio de los datos encriptados.
    salt = datos_encriptados[:16]
    datos_encriptados = datos_encriptados[16:]

    # Derivación de la clave utilizando el mismo salt y algoritmo PBKDF2HMAC.
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    clave_derivada = kdf.derive(clave)

    # Creación de un objeto Cipher para descifrar los datos usando AES en modo CFB.
    cipher = Cipher(algorithms.AES(clave_derivada), modes.CFB(salt), backend=default_backend())
    decryptor = cipher.decryptor()
    datos_desencriptados = decryptor.update(datos_encriptados) + decryptor.finalize()

    # Nombre del archivo desencriptado.
    nombre_archivo = "desencriptado_" + os.path.basename(ruta)
    ruta_archivo_desencriptado = os.path.join(ruta_guardado, nombre_archivo)

    # Escritura de los datos desencriptados en un nuevo archivo.
    with open(ruta_archivo_desencriptado, "wb") as archivo_desencriptado:
        archivo_desencriptado.write(datos_desencriptados)

    # Informa al usuario que el archivo ha sido desencriptado y guardado exitosamente.
    print(Fore.BLACK + Back.GREEN + "Archivo desencriptado y guardado en {} exitosamente.".format(ruta_archivo_desencriptado) + Style.RESET_ALL)

# Definición de la función principal para encriptar o desencriptar archivos.
def encriptar_desencriptar_main():
    while True:
        clear_screen()
        banner()
        # Solicita al usuario elegir entre encriptar, desencriptar o salir.
        opcion = input(Style.RESET_ALL + "¿Desea encriptar (1) o desencriptar (2)? 'n' para terminar: ")

        if opcion.lower() == "n":
            break

        if opcion == "1":
            ruta_archivo = obtener_ruta_archivo()
            clave = obtener_clave()
            ruta_guardado = obtener_ruta_guardado()
            encriptar_archivo(ruta_archivo, clave, ruta_guardado)

        elif opcion == "2":
            ruta_archivo = obtener_ruta_archivo()
            clave = obtener_clave()
            ruta_guardado = obtener_ruta_guardado()
            desencriptar_archivo(ruta_archivo, clave, ruta_guardado)

        else:
            # Informa al usuario que la opción ingresada no es válida.
            print(Fore.BLACK + Back.RED + "Opción no válida." + Style.RESET_ALL)

# Definición de la función para mostrar el menú principal.
def mostrar_menu():
    clear_screen()
    banner()
    print("************************")
    print("*         FILE         *")
    print("************************")
    print("*    1. Encriptar      *")
    print("*                      *")
    print("*    2. Desencriptar   *")
    print("************************")

# Función para mostrar un banner ASCII art en la consola.
def banner():
    cartel = r"""
   ___ _ _        ___                  _ _           
  | __(_) |___   / __|_  _ __ _ _ _ __| (_)__ _ _ _  
  | _|| | / -_) | (_ | || / _` | '_/ _` | / _` | ' \ 
  |_| |_|_\___|  \___|\_,_\__,_|_| \__,_|_\__,_|_||_|
    """
    print(Fore.WHITE + cartel)

# Función para limpiar la pantalla de la consola.
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Llamada a la función principal para mostrar el menú y ejecutar la encriptación o desencriptación de archivos.
if __name__ == "__main__":
    clear_screen()
    mostrar_menu()
    encriptar_desencriptar_main()
