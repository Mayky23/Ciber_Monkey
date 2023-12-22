import subprocess

def obtener_perfiles_wifi():
    perfiles = []
    try:
        process = subprocess.Popen("netsh wlan show profile", stdout=subprocess.PIPE, shell=True)
        process.wait()
        output = process.stdout.decode('utf-8')
        for line in output.split('\n'):
            if ":" in line:
                datos = line.split(":")
                if len(datos) >= 2:
                    perfiles.append(datos[1].strip())
    except Exception as e:
        print(e)

    mostrar_contrasenas(perfiles)

def mostrar_contrasenas(perfiles):
    for i, perfil in enumerate(perfiles):
        print(f"RED {i + 1}: {perfil}")
        cmd = ["netsh", "wlan", "show", "profile", perfil, "key=clear"]
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            process.wait()
            output = process.stdout.decode('utf-8')
            resultado = output.split('\n')
            contrasenas = [split_line.split(":")[1].strip() for split_line in resultado if "Contenido de la clave" in split_line]
            if contrasenas:
                for j, contrasena in enumerate(contrasenas):
                    print(f"PASSWORD {j + 1}: {contrasena}")
            else:
                print("PASSWORD 1: No encontrada")
            print("----------------------------------------------------------------------------------")
        except Exception as e:
            print(e)

def wifi_scanner_main():
    print("¿Desea escanear las redes WiFi? (s/n): ")
    respuesta = input().strip().lower()

    if respuesta == "s":
        obtener_perfiles_wifi()
    else:
        print("Programa finalizado.")
