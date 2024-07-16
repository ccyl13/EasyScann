#!/usr/bin/env python3

import subprocess
from termcolor import colored, cprint

def scan_network(network_range):
    active_devices = []

    try:
        cmd = f"sudo nmap -sP {network_range}"  # Escaneo de ping simple con nmap
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            lines = output.decode().splitlines()
            for line in lines:
                if "Nmap scan report for" in line:
                    parts = line.split()
                    ip_address = parts[4]
                    active_devices.append(ip_address)

        return active_devices

    except Exception as e:
        print(f"Error al escanear la red: {str(e)}")
        return active_devices

def main():
    cprint("\n  _____                ____                        ", 'blue', attrs=['bold'])
    cprint(" | ____|__ _ ___ _   _/ ___|  ___ __ _ _ __  _ __  ", 'blue', attrs=['bold'])
    cprint(" |  _| / _` / __| | | \___ \ / __/ _` | '_ \| '_ \ ", 'blue', attrs=['bold'])
    cprint(" | |__| (_| \__ \ |_| |___) | (_| (_| | | | | | | |", 'blue', attrs=['bold'])
    cprint(" |_____\__,_|___/\__, |____/ \___\__,_|_| |_|_| |_|", 'blue', attrs=['bold'])
    cprint("                 |___/                              ", 'blue', attrs=['bold'])
    print("\nHerramienta para escanear y listar dispositivos activos en la red local.")
    print("Desarrollada por ", end='')
    cprint("Thomas O'Neil", 'blue', attrs=['bold'])
    print()

    network_range = input("Ingrese el rango de red (por ejemplo, 192.168.1.0/24): ").strip()

    print(f"\nEscaneando la red {network_range}, por favor espere...\n")
    active_devices = scan_network(network_range)

    if active_devices:
        print("Detalles de dispositivos activos en la red:")
        for device in active_devices:
            cprint(f"  - IP: {device}", 'green')
            try:
                cmd = f"sudo nmap -O {device}"  # Escaneo de detección de sistema operativo con nmap
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()

                if process.returncode == 0:
                    lines = output.decode().splitlines()
                    for line in lines:
                        if "MAC Address" in line:
                            mac_address = line.split("MAC Address: ")[1].strip()
                            cprint(f"    MAC Address: {mac_address}", 'cyan')
                        elif "Device type" in line:
                            device_type = line.split("Device type: ")[1].strip()
                            cprint(f"    Device type: {device_type}", 'cyan')
                        elif "Running" in line:
                            os_info = line.split(": ")[1].strip()
                            cprint(f"    OS Info: {os_info}", 'cyan')
                        elif "Aggressive OS guesses" in line:
                            os_guess = line.split(": ")[1].strip()
                            cprint(f"    OS Guesses: {os_guess}", 'cyan')
                        elif "Host is up" in line:
                            hostname = line.split("Host is up ")[1].split(" ")[0].strip()
                            cprint(f"    Hostname: {hostname}", 'cyan')

            except Exception as e:
                print(f"Error al obtener detalles de {device}: {str(e)}")
    else:
        print("No se encontraron dispositivos activos en la red.")

if __name__ == "__main__":
    main()
