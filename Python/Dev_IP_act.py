import socket

def descubrir_host():
    while True:
        try:
            input_value = input("Ingrese una dirección IP (o escriba 'salir' para salir): ")

            if input_value.lower() == "salir":
                print("Saliendo del programa...")
                break

            ip = socket.gethostbyname(input_value)

            if ping(ip):
                print(f"La dirección IP {ip} ESTÁ ACTIVA.")
            else:
                print(f"La dirección IP {ip} NO ESTÁ ACTIVA.")
        except socket.gaierror:
            print("Dirección IP inválida. Ingrese una dirección IP válida.")
        except Exception as e:
            print(f"Ocurrió un error: {e}. Por favor, inténtelo de nuevo.")

def ping(ip):
    try:
        with socket.create_connection((ip, 80), timeout=5):
            return True
    except (socket.timeout, socket.error):
        return False

def host_discovery_main():
    descubrir_host()
