import pywifi
from pywifi import const
import nmap

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
    if akm in TIPOS_AUTENTICACION:
        return TIPOS_AUTENTICACION[akm]
    else:
        return "Desconocido"

def obtener_tipo_cifrado(cipher):

    """Función para obtener el tipo de cifrado según el mapeo definido."""
    if cipher in TIPOS_CIFRADO:
        return TIPOS_CIFRADO[cipher]
    else:
        return "Desconocido"

def escanear_redes():

    """Función para escanear redes WiFi disponibles."""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    
    iface.scan()
    resultados = iface.scan_results()

    return resultados

def escanear_puertos(ip):

    """Función para escanear puertos abiertos en una dirección IP."""
    nm = nmap.PortScanner()

    # Escanea todos los puertos en la dirección IP especificada y devuelve los abiertos
    nm.scan(hosts=ip, arguments='-p 1-65535 --open')
    puertos_abiertos = []
    for host in nm.all_hosts():
        if nm[host].has_tcp(ports=''):
            for port in nm[host]['tcp'].keys():
                puertos_abiertos.append(port)
    return puertos_abiertos

def wifi_scanner_main():
    
    """Función principal para escanear redes WiFi y sus puertos abiertos."""
    resultados = escanear_redes()

    if len(resultados) == 0:
        print("No se encontraron redes WiFi disponibles.")
        return

    print("Redes WiFi disponibles:")
    for resultado in resultados:
        nombre_red = resultado.ssid
        seguridad = obtener_tipo_autenticacion(resultado.akm[0])
        cifrado = obtener_tipo_cifrado(resultado.cipher[0])

        print(f"Nombre: {nombre_red}")
        print(f"Tipo de seguridad: {seguridad}")
        print(f"Tipo de cifrado: {cifrado}")
        
        # Obtener dirección IP del punto de acceso
        ip = resultado.bssid
        
        # Escanear puertos abiertos en la red
        puertos_abiertos = escanear_puertos(ip)
        if puertos_abiertos:
            print("Puertos abiertos:")
            for puerto in puertos_abiertos:
                print(f"    Puerto: {puerto}")
        else:
            print("No se encontraron puertos abiertos en esta red.")
        
        print("----------------------------------------------------------------------------------")

wifi_scanner_main()
