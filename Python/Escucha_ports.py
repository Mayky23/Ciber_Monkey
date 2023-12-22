import socket
import subprocess

def escucha_puertos():
    try:
        port = int(input("Ingrese el puerto: "))

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", port))
        server_socket.listen(1)

        print(f"Esperando conexiones entrantes en el puerto {port}...")

        client_socket, addr = server_socket.accept()
        print(f"Conexión establecida desde: {addr[0]}:{addr[1]}")

        isocket = client_socket.makefile("r")
        osocket = client_socket.makefile("w")

        while True:
            command = isocket.readline().strip()

            if command.lower() == "exit":
                break

            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            process.wait()

            command_output = process.stdout.read()
            osocket.write(command_output)
            osocket.flush()

        client_socket.close()
        server_socket.close()

    except (socket.error, ValueError, subprocess.CalledProcessError) as e:
        print(f"Ocurrió un error: {e}")

def escucha_puertos_main():
    escucha_puertos()
