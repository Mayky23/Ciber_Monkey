import os
import platform
import ipaddress

def listar_ips_activas(direccion_ip):
    """Función para listar todas las direcciones IP activas en la subred local."""
    
    # Obtenemos la parte de la dirección IP local sin la máscara de red
    direccion_ip_obj = ipaddress.ip_address(direccion_ip)

    # Construimos la red local a partir de la dirección IP local
    red_local = ipaddress.IPv4Network(f"{direccion_ip_obj}/24", strict=False)

    print(f"Escaneando IPs en la subred local {red_local}...\n")

    # Lista para almacenar las IPs activas
    ips_activas = []

    # Iteramos sobre cada dirección IP en la subred local
    for ip in red_local.hosts():
        ip = str(ip)
        if platform.system().lower() == "windows":
            response = os.system(f"ping -n 1 {ip} > nul")
        else:
            response = os.system(f"ping -c 1 {ip} > /dev/null")

        # Verificamos si la respuesta del ping indica que la IP está activa
        if response == 0:
            ips_activas.append(ip)

    return ips_activas

def host_discovery_main():
    direccion_ip = input("Inserta IP del host de la red: ").strip()

    ips_activas = listar_ips_activas(direccion_ip)

    if ips_activas:
        print("\nDirecciones IP activas encontradas en la subred local:")
        for ip in ips_activas:
            print(ip)
    else:
        print("\nNo se encontraron direcciones IP activas en la subred local.")

if __name__ == "__main__":
    host_discovery_main()
