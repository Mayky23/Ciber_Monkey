import os # interactuar con el sistema operativo
import asyncio 
""" escribir código concurrente utilizando la sintaxis async/await. 
Esto permite que ciertas operaciones, como la entrada/salida (E/S) bloqueante, 
se realicen de manera asíncrona, lo que significa que el intérprete de Python puede 
continuar ejecutando otras partes del programa mientras espera que se completen estas operaciones.
"""
import platform # obtener información sobre la plataforma en la que se está ejecutando Python, como el nombre del sistema operativo.
import ipaddress # manipular direcciones IP y subredes.


# Se importa la biblioteca colorama para el manejo de colores en la consola.
from colorama import *

# Función asincrónica para realizar un ping a una dirección IP.
async def ping(ip):
    # Se determina el sistema operativo para definir el comando ping adecuado.
    if platform.system().lower() == "windows":
        comando_ping = ["ping", "-n", "1", ip]
    else:
        comando_ping = ["ping", "-c", "1", ip]

    # Se crea un proceso para ejecutar el comando ping.
    proceso = await asyncio.create_subprocess_exec(*comando_ping, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proceso.communicate()

    # Se devuelve True si el ping fue exitoso y False en caso contrario.
    return proceso.returncode == 0 and ("bytes=" in str(stdout))

# Función asincrónica para listar las direcciones IP activas en la subred local.
async def listar_ips_activas(direccion_ip):
    """Función para listar todas las direcciones IP activas en la subred local."""
    try:
        # Se crea un objeto de dirección IP a partir de la cadena proporcionada.
        direccion_ip_obj = ipaddress.ip_address(direccion_ip)
    except ValueError:
        # Manejo de excepción si la dirección IP proporcionada es inválida.
        print(Fore.BLACK + Back.RED + "Dirección IP inválida. Inténtelo de nuevo." + Style.RESET_ALL)
        return

    # Se define la red local utilizando la dirección IP y la máscara de subred /24.
    red_local = ipaddress.IPv4Network(f"{direccion_ip_obj}/24", strict=False)

    # Se imprime un mensaje indicando que se está escaneando la subred local.
    print(f"\nEscaneando IPs en la subred local {red_local}...\n")

    # Se itera sobre todas las direcciones IP en la subred local.
    for ip in red_local:
        # Se verifica si la dirección IP está activa realizando un ping.
        if await ping(str(ip)):
            # Si el ping es exitoso, se imprime la dirección IP activa.
            print(ip)

# Función para mostrar un banner en la consola.
def banner():
    clear_screen()
    cartel = r"""
     _      _   _           ___ ___ 
    /_\  __| |_(_)_ _____  |_ _| _ \
   / _ \/ _|  _| \ V / -_)  | ||  _/
  /_/ \_\__|\__|_|\_/\___| |___|_|  
                                       
    """
    print(Fore.LIGHTYELLOW_EX +  cartel)

# Función para limpiar la pantalla de la consola.
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Función principal para descubrir hosts en la red.
def host_discovery_main():
    while True:
        banner()
        print("************************************************")
        
        # Se solicita al usuario que ingrese la dirección IP del host de la red.
        direccion_ip = input(Style.RESET_ALL +"Inserta IP del host de la red (ej:10.192.104.0) o 'n' para terminar: ")

        # Si el usuario ingresa 'n', se termina el programa.
        if direccion_ip.lower() == "n":
            break
        
        # Se ejecuta la función asincrónica para listar las direcciones IP activas en la subred local.
        asyncio.run(listar_ips_activas(direccion_ip))

# Bloque principal para ejecutar la función principal si este script es ejecutado directamente.
if __name__ == "__main__":
    host_discovery_main()
