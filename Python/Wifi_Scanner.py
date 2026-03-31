import time
import ipaddress
import shutil
import subprocess
from typing import List, Dict, Any

from colorama import Fore, Style, init
from Python.ui import clear_screen, draw_banner, pause, print_error, print_info, print_ok

try:
    import pywifi
    from pywifi import const
except Exception:
    pywifi = None
    const = None

try:
    import scapy.all as scapy
except Exception:
    scapy = None

init(autoreset=True)
COMMON_ASCII = r"""
 Wifi Scanner
"""
BANNER_COLOR = "\033[33m"

# ======== Mapeos WiFi ========

TIPOS_AUTENTICACION = {}
TIPOS_CIFRADO = {}

if const is not None:
    TIPOS_AUTENTICACION = {
        const.AKM_TYPE_NONE: "Ninguna",
        const.AKM_TYPE_WPA: "WPA/WPA2 (Enterprise)",
        const.AKM_TYPE_WPAPSK: "WPA-PSK",
        const.AKM_TYPE_WPA2PSK: "WPA2-PSK",
        const.AKM_TYPE_WPA2: "WPA2 (Enterprise)",
    }

    TIPOS_CIFRADO = {
        const.CIPHER_TYPE_NONE: "Ninguno",
        const.CIPHER_TYPE_CCMP: "CCMP (AES)",
        const.CIPHER_TYPE_TKIP: "TKIP",
    }


def obtener_tipo_autenticacion(akm: int) -> str:
    return TIPOS_AUTENTICACION.get(akm, "Desconocido")


def obtener_tipo_cifrado(cipher: int) -> str:
    return TIPOS_CIFRADO.get(cipher, "Desconocido")


def banner():
    draw_banner("", COMMON_ASCII, "Descubrimiento LAN, puertos y redes WiFi", BANNER_COLOR)


# ======== Validación red ========

def parse_network(net_str: str) -> ipaddress.IPv4Network:
    """
    Acepta '192.168.1.0/24' y valida.
    """
    net = ipaddress.ip_network(net_str.strip(), strict=False)
    if not isinstance(net, ipaddress.IPv4Network):
        raise ValueError("Solo se soporta IPv4 en este módulo.")
    return net


# ======== LAN scan (ARP) ========

def escanear_red_lan(subnet: str, timeout: float = 1.0) -> List[Dict[str, str]]:
    """
    Descubrimiento ARP (LAN local). Requiere permisos elevados en muchos sistemas.
    Devuelve lista de {ip, mac}.
    """
    if scapy is None:
        raise RuntimeError("Falta scapy. Instala dependencias con requirements.txt.")
    red = parse_network(subnet)

    # Construimos ARP request para todo el rango
    arp_request = scapy.ARP(pdst=str(red))
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    try:
        answered = scapy.srp(packet, timeout=timeout, verbose=False)[0]
    except PermissionError:
        # Windows/Linux/macOS pueden lanzar PermissionError
        raise PermissionError("Permisos insuficientes: ejecuta como admin/root para ARP scan.")
    except OSError as e:
        raise OSError(f"Error de socket al usar scapy: {e}")

    hosts: List[Dict[str, str]] = []
    for _, recv in answered:
        hosts.append({"ip": recv.psrc, "mac": recv.hwsrc})

    # Ordenar por IP
    hosts.sort(key=lambda h: ipaddress.ip_address(h["ip"]))
    return hosts


# ======== Port scan (Nmap) ========

def escanear_puertos(ip: str, profile: str = "top") -> List[int]:
    """
    Escaneo de puertos con nmap.
    profile:
      - 'top'  -> top 1000 puertos (rápido)
      - 'full' -> 1-65535 (lento/ruidoso)
      - 'web'  -> 80,443,8080,8443
    """
    if not shutil.which("nmap"):
        raise RuntimeError("No se encontro el binario nmap en PATH.")

    if profile == "full":
        command = ["nmap", "-sS", "-p", "1-65535", "--open", "-oG", "-", ip]
    elif profile == "web":
        command = ["nmap", "-sS", "-p", "80,443,8080,8443", "--open", "-oG", "-", ip]
    else:
        command = ["nmap", "--top-ports", "1000", "-sS", "--open", "-oG", "-", ip]

    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    abiertos: List[int] = []
    for line in proc.stdout.splitlines():
        if "Ports:" not in line:
            continue
        _, ports_blob = line.split("Ports:", 1)
        for entry in ports_blob.split(","):
            fields = entry.strip().split("/")
            if len(fields) >= 2 and fields[1] == "open" and fields[0].isdigit():
                abiertos.append(int(fields[0]))
    return sorted(set(abiertos))


# ======== WiFi scan (solo info) ========

def escanear_redes_wifi(scan_wait_s: float = 3.0):
    """
    Escanea redes WiFi disponibles (SSID/BSSID/seguridad/cifrado).
    Nota: pywifi depende mucho del SO/driver.
    """
    if pywifi is None:
        print_error("Falta pywifi. Instala dependencias con requirements.txt.")
        return []
    try:
        wifi = pywifi.PyWiFi()
        ifaces = wifi.interfaces()
        if not ifaces:
            print_error("No se encontraron interfaces WiFi disponibles.")
            return []

        iface = ifaces[0]
        iface.scan()
        time.sleep(scan_wait_s)  # importante para que se rellenen resultados
        return iface.scan_results()

    except Exception as e:
        print_error(f"Error al escanear redes WiFi: {e}")
        return []


def format_wifi_result(r) -> Dict[str, Any]:
    ssid = r.ssid or "<hidden>"
    bssid = getattr(r, "bssid", "") or ""
    signal = getattr(r, "signal", None)

    # akm/cipher suelen ser listas
    akm = r.akm[0] if getattr(r, "akm", None) and const is not None else 0
    cipher = r.cipher[0] if getattr(r, "cipher", None) and const is not None else 0

    return {
        "ssid": ssid,
        "bssid": bssid,
        "signal": signal,
        "auth": obtener_tipo_autenticacion(akm),
        "cipher": obtener_tipo_cifrado(cipher),
    }


# ======== Main ========

def wifi_scanner_main():
    while True:
        banner()
        print("1. LAN")
        print("2. WiFi")
        print("n. Salir")

        opcion = input(Style.RESET_ALL + "\nSeleccione (1/2/n): ").strip().lower()
        if opcion == "n":
            return

        if opcion == "1":
            subnet = input("Ingrese la subred (ej: 192.168.1.0/24): ").strip()
            try:
                hosts = escanear_red_lan(subnet)
            except ValueError as e:
                print_error(f"Subred inválida: {e}")
                pause()
                continue
            except PermissionError as e:
                print_error(str(e))
                pause()
                continue
            except Exception as e:
                print_error(f"Error escaneando LAN: {e}")
                pause()
                continue

            if not hosts:
                print_error("No se encontraron hosts en la red LAN.")
                pause()
                continue

            print_info(f"Hosts encontrados: {len(hosts)}")
            profile = input("Perfil de puertos [top/web/full] (default=top): ").strip().lower() or "top"

            for h in hosts:
                print_ok(f"\nHost: {h['ip']}  MAC: {h['mac']}")
                try:
                    puertos = escanear_puertos(h["ip"], profile=profile)
                except Exception as e:
                    print_error(f"Error escaneando puertos en {h['ip']}: {e}")
                    continue

                if puertos:
                    print_info("Puertos abiertos: " + ", ".join(map(str, puertos)))
                else:
                    print_info("Sin puertos abiertos (según perfil).")

            pause("\nPulsa Enter para volver al menu...")
            continue

        if opcion == "2":
            resultados = escanear_redes_wifi()
            if not resultados:
                print_error("No se encontraron redes WiFi disponibles.")
                pause()
                continue

            print_info(f"Redes WiFi detectadas: {len(resultados)}\n")
            for r in resultados:
                d = format_wifi_result(r)
                print_ok(f"SSID: {d['ssid']}")
                print(f"  BSSID:   {d['bssid']}")
                print(f"  Señal:   {d['signal']}")
                print(f"  Auth:    {d['auth']}")
                print(f"  Cifrado: {d['cipher']}")
                print(Style.RESET_ALL + "----------------------------------------------")

            print_info("Nota: No se escanean puertos por BSSID (es MAC, no IP).")
            print_info("Si quieres escanear puertos, usa la opción LAN sobre tu subnet actual.")
            pause("\nPulsa Enter para volver al menu...")
            continue

        print_error("Opción no válida.")
        time.sleep(1)


if __name__ == "__main__":
    clear_screen()
    wifi_scanner_main()
