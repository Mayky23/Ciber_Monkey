import asyncio
import platform
import ipaddress
import subprocess

async def ping(ip):
    if platform.system().lower() == "windows":
        comando_ping = ["ping", "-n", "1", ip]
    else:
        comando_ping = ["ping", "-c", "1", ip]

    proceso = await asyncio.create_subprocess_exec(*comando_ping, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proceso.communicate()

    return ip if proceso.returncode == 0 and ("bytes=" in str(stdout)) else None

async def listar_ips_activas(direccion_ip):
    """Función para listar todas las direcciones IP activas en la subred local."""
    
    direccion_ip_obj = ipaddress.ip_address(direccion_ip)
    red_local = ipaddress.IPv4Network(f"{direccion_ip_obj}/24", strict=False)

    print(f"Escaneando IPs en la subred local {red_local}...\n")

    ips_activas = []

    tasks = []
    for ip in red_local:
        tasks.append(ping(str(ip)))

    resultados = await asyncio.gather(*tasks)
    ips_activas = [ip for ip in resultados if ip]

    return ips_activas

def banner():
    cartel = r"""
     _      _   _           ___ ___ 
    /_\  __| |_(_)_ _____  |_ _| _ \
   / _ \/ _|  _| \ V / -_)  | ||  _/
  /_/ \_\__|\__|_|\_/\___| |___|_|  
                                       
    """
    print(cartel)

def host_discovery_main():

    banner()
    print("************************************************")
    
    direccion_ip = input("Inserta IP del host de la red (ej:10.192.104.0): ").strip()

    loop = asyncio.get_event_loop()
    ips_activas = loop.run_until_complete(listar_ips_activas(direccion_ip))
    loop.close()

    if ips_activas:
        print("\nDirecciones IP activas encontradas en la subred local:")
        for ip in ips_activas:
            print(ip)
    else:
        print("\nNo se encontraron direcciones IP activas en la subred local.")

if __name__ == "__main__":
    host_discovery_main()
