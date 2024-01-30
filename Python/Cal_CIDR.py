import ipaddress

def get_prefix_length(ip):
    # Obtiene la dirección IP en forma de lista de bytes
    bytes_list = ip.packed

    # Inicializa la máscara de subred y el índice de bits
    mask = 0

    # Itera a través de los bytes de la dirección IP
    for byte in bytes_list:

        # Itera a través de los bits de cada byte
        for bit_index in range(8):
            # Si el bit es 1, incrementa la máscara de subred
            if (byte & (1 << (7 - bit_index))) != 0:
                mask += 1

    # Retorna la máscara de subred en formato CIDR
    return mask

def banner():
    cartel = r"""
       __      _       ___ ___ ___  ___
     / __|__ _| |__   / __|_ _|   \| _ \                                                \t     
    | (__/ _` | / _| | (__ | || |) |   /   
     \___\__,_|_\__|  \___|___|___/|_|_\
                                             
    """
    print(cartel)

def calculate_cidr():
    
    banner()
    
    while True:
        print("************************************************")
        ip_string = input("\nIngrese una dirección IP (o 'n' para terminar): ")

        if ip_string.lower() == "n":
            break

        try:
            ip = ipaddress.IPv4Address(ip_string)
            prefix_length = get_prefix_length(ip)
            print(f"{ip} / {prefix_length}")
        except ValueError:
            print("Dirección IP inválida. Inténtelo de nuevo.")

calculate_cidr()
