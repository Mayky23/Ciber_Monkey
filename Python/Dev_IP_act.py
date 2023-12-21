import socket

def descubrir_host():
    while True:
        try:
            # Solicita la dirección IP al usuario
            input_value = input("Ingrese una dirección IP (o escriba 'salir' para salir): ")

            if input_value.lower() == "salir":
                print("Saliendo del programa...")
                break

            # Convierte la dirección IP a un objeto InetAddress
            ip = socket.gethostbyname(input_value)

            # Realiza un ping a la dirección IP para verificar si está activa
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
        # Intenta establecer una conexión con el host en el puerto 80
        with socket.create_connection((ip, 80), timeout=5):
            return True
    except (socket.timeout, socket.error):
        return False

if __name__ == "__main__":
    descubrir_host()
