import socket
import subprocess

def escucha_puertos(puerto, direccion_ip):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((direccion_ip, puerto))
        server_socket.listen(1)

        print(f"Esperando conexiones entrantes en {direccion_ip}:{puerto}...")

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
    direccion_ip = input("Ingrese la dirección IP en la que desea estar a la escucha: ")
    puerto = int(input("Ingrese el puerto en el que desea estar a la escucha: "))

    escucha_puertos(puerto, direccion_ip)

if __name__ == "__main__":
    escucha_puertos_main()
