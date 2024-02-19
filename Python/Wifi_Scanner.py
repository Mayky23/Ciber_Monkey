import os
import pywifi
from pywifi import const
import nmap
import scapy.all as scapy
from colorama import *

# Mapeo de tipos de autenticación para mostrar descripciones más legibles
TIPOS_AUTENTICACION = {
    const.AKM_TYPE_NONE: "Ninguna",
    const.AKM_TYPE_WPA: "WPA/WPA2",
    const.AKM_TYPE_WPAPSK: "WPA-PSK",
    const.AKM_TYPE_WPA2PSK: "WPA2-PSK",
    const.AKM_TYPE_WPA2: "WPA2",
}

# Mapeo de tipos de cifrado para mostrar descripciones más legibles
TIPOS_CIFRADO = {
    const.CIPHER_TYPE_NONE: "Ninguno",
    const.CIPHER_TYPE_CCMP: "CCMP",
    const.CIPHER_TYPE_TKIP: "TKIP",
}

def obtener_tipo_autenticacion(akm):
    """Función para obtener el tipo de autenticación según el mapeo definido."""
    return TIPOS_AUTENTICACION.get(akm, "Desconocido")

def obtener_tipo_cifrado(cipher):
    """Función para obtener el tipo de cifrado según el mapeo definido."""
    return TIPOS_CIFRADO.get(cipher, "Desconocido")

def escanear_red_lan(ip):
    """Función para escanear hosts en la red LAN."""
    subnet = ip + "/24"  # Agregar /24 para escanear toda la subred
    arp_request = scapy.ARP(pdst=subnet)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    hosts = []
    for element in answered_list:
        host = {"ip": element[1].psrc}
        hosts.append(host)
    return hosts

def escanear_puertos(ip):
    """Función para escanear puertos abiertos en una dirección IP."""
    nm = nmap.PortScanner()
    nm.scan(hosts=ip, arguments='-p 1-65535 --open')
    puertos_abiertos = []
    for host in nm.all_hosts():
        if 'tcp' in nm[host]:
            for port in nm[host]['tcp'].keys():
                puertos_abiertos.append(port)
    return puertos_abiertos

def escanear_redes_wifi():
    """Función para escanear redes WiFi disponibles."""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    return iface.scan_results()

def banner():
    cartel = r"""
  __      ___  __ _   ___
  \ \    / (_)/ _(_) / __| __ __ _ _ _  _ _  ___ _ _
   \ \/\/ /| |  _| | \__ \/ _/ _` | ' \| ' \/ -_) '_|
    \_/\_/ |_|_| |_| |___/\__\__,_|_||_|_||_\___|_|

    """
    clear_screen()
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + cartel)

def wifi_scanner_main():
    """Función principal para escanear redes WiFi y sus puertos abiertos."""
    banner()
    print("************************")
    print("*   TIPO DE CONEXIÓN:  *")
    print("************************")
    print("*      1. LAN          *")
    print("*                      *")
    print("*      2. WiFi         *")
    print("************************")

    opcion = input(Style.RESET_ALL + "\nSeleccione el tipo de conexión (1/2) o n para salir: ").strip()

    if opcion.lower() == 'n':
        return  # Salir del programa si se ingresa 'n'

    if opcion == "1":
        subnet = input("Ingrese la subred de su LAN (por ejemplo, 192.168.1.1/24): ").strip()
        hosts = escanear_red_lan(subnet)
        if not hosts:
            print(Fore.BLACK + Back.RED +"No se encontraron hosts en la red LAN.")
            return
        print("Hosts en la red LAN:")
        for host in hosts:
            print("IP:", host["ip"])
            puertos_abiertos = escanear_puertos(host["ip"])
            if puertos_abiertos:
                print("Puertos abiertos:")
                for puerto in puertos_abiertos:
                    print("    Puerto:", puerto)
            else:
                print(Fore.BLACK + Back.RED +"No se encontraron puertos abiertos en este host.")
            print(Style.RESET_ALL +"----------------------------------------------")

    elif opcion == "2":
        resultados = escanear_redes_wifi()
        if not resultados:
            print(Fore.BLACK + Back.RED +"No se encontraron redes WiFi disponibles.")
            return
        print(Style.RESET_ALL + "Redes WiFi disponibles:")
        for resultado in resultados:
            nombre_red = resultado.ssid
            seguridad = obtener_tipo_autenticacion(resultado.akm[0])
            cifrado = obtener_tipo_cifrado(resultado.cipher[0])
            print(f"Nombre: {nombre_red}")
            print(f"Tipo de seguridad: {seguridad}")
            print(f"Tipo de cifrado: {cifrado}")
            ip = resultado.bssid
            puertos_abiertos = escanear_puertos(ip)
            if puertos_abiertos:
                print("Puertos abiertos:")
                for puerto in puertos_abiertos:
                    print(f"    Puerto: {puerto}")
            else:
                print(Fore.BLACK + Back.RED +"No se encontraron puertos abiertos en esta red.")
            print(Style.RESET_ALL + "----------------------------------------------")

    else:
        print(Fore.BLACK + Back.RED + "Opción no válida." + Style.RESET_ALL)
        clear_screen()
        wifi_scanner_main()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    clear_screen()
    wifi_scanner_main()
