"""

Usando Sublist3r como un módulo en tus scripts de Python
Ejemplo

import sublist3r 
subdomains = sublist3r.main(domain, no_threads, savefile, ports, silent, verbose, enable_bruteforce, engines)

La función principal devolverá un conjunto de subdominios únicos encontrados por Sublist3r.

Function Usage:

domain: The domain you want to enumerate subdomains of.
savefile: save the output into text file.
ports: specify a comma-sperated list of the tcp ports to scan.
silent: set sublist3r to work in silent mode during the execution (helpful when you don't need a lot of noise).
verbose: display the found subdomains in real time.
enable_bruteforce: enable the bruteforce module.
engines: (Optional) to choose specific engines.
Example to enumerate subdomains of Yahoo.com:

import sublist3r 
subdomains = sublist3r.main('yahoo.com', 40, 'yahoo_subdomains.txt', ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)

"""

import sublist3r

def List_Subdominios_main(domain, no_threads=40, savefile=None, ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None):
    """
    Enumera los subdominios de un dominio dado utilizando Sublist3r.

    Args:
        domain (str): El dominio del cual se quieren enumerar los subdominios.
        no_threads (int): Número de hilos para usar durante la enumeración (por defecto 40).
        savefile (str): Nombre del archivo donde guardar la salida (por defecto None).
        ports (str): Lista de puertos TCP separados por comas para escanear (por defecto None).
        silent (bool): Establece Sublist3r para trabajar en modo silencioso durante la ejecución (útil cuando no se necesita mucho ruido) (por defecto False).
        verbose (bool): Muestra los subdominios encontrados en tiempo real (por defecto False).
        enable_bruteforce (bool): Habilita el módulo de fuerza bruta (por defecto False).
        engines (list): (Opcional) para elegir motores específicos (por defecto None).

    Returns:
        set: Conjunto de subdominios únicos encontrados por Sublist3r.
    """
    try:
        subdomains = sublist3r.main(domain, no_threads, savefile, ports, silent, verbose, enable_bruteforce, engines)
        return subdomains
    except Exception as e:
        print(f"Error: {e}")
        return set()

def main():
    domain = input("Introduce el dominio para enumerar subdominios: ")
    subdomains = List_Subdominios_main(domain)
    print(f"Subdominios encontrados para {domain}:")
    for subdomain in subdomains:
        print(subdomain)

if __name__ == "__main__":
    main()




