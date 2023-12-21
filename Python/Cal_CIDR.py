import ipaddress

def get_prefix_length(ip):
    # Obtiene la dirección IP en forma de lista de bytes
    bytes_list = ip.packed

    # Inicializa la máscara de subred y el índice de bits
    mask = 0
    bit_index = 7

    # Itera a través de los bytes de la dirección IP
    for byte in bytes_list:
        # Itera a través de los bits de cada byte
        for i in range(8):
            # Si el bit es 1, incrementa la máscara de subred
            if (byte & (1 << bit_index)) != 0:
                mask += 1

            # Disminuye el índice de bits
            bit_index -= 1

    # Retorna la máscara de subred en formato CIDR
    return mask

def main():
    while True:
        # Lee la dirección IP desde la entrada del usuario
        ip_string = input("\nIngrese una dirección IP (o 'no' para terminar): ")

        if ip_string.lower() == "no":
            # Si el usuario escribe "no", sale del bucle
            break

        try:
            # Convierte la dirección IP a un objeto ipaddress.IPv4Address
            ip = ipaddress.IPv4Address(ip_string)

            # Calcula la máscara de subred en formato CIDR
            prefix_length = get_prefix_length(ip)
            print(f"{ip} / {prefix_length}")
        except ValueError:
            print("Dirección IP inválida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()
