import socket
from urllib.parse import getservbyport

def scan_ports(host, start_port, end_port):
    active_ports = []
    try:
        for port in range(start_port, end_port + 1):
            with socket.create_connection((host, port), timeout=1) as con:
                active_ports.append(port)
    except (socket.timeout, socket.error):
        pass
    return active_ports

def main():
    host = input("Ingrese la dirección de host: ")
    start_port = int(input("Ingrese el puerto inicial: "))
    end_port = int(input("Ingrese el puerto final: "))

    try:
        active_ports = scan_ports(host, start_port, end_port)
        if active_ports:
            print("Puertos activos:")
            for port in active_ports:
                try:
                    service_name = getservbyport(port)
                except OSError:
                    service_name = "Desconocido"
                print(f"ACTIVO: {service_name} ({port})")
        else:
            print(f"No se encontraron puertos activos en {host}.")
    except ValueError:
        print("Error: Ingrese números válidos para los puertos.")

if __name__ == "__main__":
    main()
