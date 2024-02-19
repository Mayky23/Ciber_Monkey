import os
import asyncio
import platform
import ipaddress


from colorama import *

async def ping(ip):
    if platform.system().lower() == "windows":
        comando_ping = ["ping", "-n", "1", ip]
    else:
        comando_ping = ["ping", "-c", "1", ip]

    proceso = await asyncio.create_subprocess_exec(*comando_ping, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proceso.communicate()

    return proceso.returncode == 0 and ("bytes=" in str(stdout))

async def listar_ips_activas(direccion_ip):
    """Función para listar todas las direcciones IP activas en la subred local."""
    try:
        direccion_ip_obj = ipaddress.ip_address(direccion_ip)
    except ValueError:
        print(Fore.BLACK + Back.RED + "Dirección IP inválida. Inténtelo de nuevo.")
        return

    red_local = ipaddress.IPv4Network(f"{direccion_ip_obj}/24", strict=False)

    print(f"\nEscaneando IPs en la subred local {red_local}...\n")

    for ip in red_local:
        if await ping(str(ip)):
            print(ip)

def banner():
    clear_screen()
    cartel = r"""
     _      _   _           ___ ___ 
    /_\  __| |_(_)_ _____  |_ _| _ \
   / _ \/ _|  _| \ V / -_)  | ||  _/
  /_/ \_\__|\__|_|\_/\___| |___|_|  
                                       
    """
    print(Fore.LIGHTYELLOW_EX +  cartel)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def host_discovery_main():
    while True:
        banner()
        print("************************************************")
        
        direccion_ip = input(Style.RESET_ALL +"Inserta IP del host de la red (ej:10.192.104.0) o 'n' para terminar: ")

        if direccion_ip.lower() == "n":
            break
        
        asyncio.run(listar_ips_activas(direccion_ip))

if __name__ == "__main__":
    host_discovery_main()
