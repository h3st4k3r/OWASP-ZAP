#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import requests

def install_requirements():
    """Installs required packages on a Debian-based system."""
    print("Instalando los requisitos...")
    subprocess.run(["sudo", "apt", "update"], check=True)
    subprocess.run(["sudo", "apt", "install", "-y", "docker.io", "python3-pip"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "--now", "docker"], check=True)
    print("Requisitos instalados correctamente.")

def start_owasp_zap():
    """Starts the OWASP ZAP Docker container."""
    print("Iniciando OWASP ZAP...")
    subprocess.run([
        "docker", "run", "-d", "--name", "owasp-zap", "-u", "zap",
        "-p", "8080:8080", "zaproxy/zap-weekly:latest",
        "zap.sh", "-daemon", "-host", "0.0.0.0", "-port", "8080",
        "-config", "api.addrs.addr.name=.*", "-config", "api.addrs.addr.regex=true"
    ], check=True)
    print("OWASP ZAP iniciado correctamente. Esperando a que se inicialice...")
    time.sleep(15) 

def stop_owasp_zap():
    """Stops and removes the OWASP ZAP container."""
    print("Deteniendo OWASP ZAP...")
    subprocess.run(["docker", "rm", "-f", "owasp-zap"], check=True)
    print("OWASP ZAP detenido y eliminado correctamente.")

def perform_scan(domain):
    """Performs a Spider and Active Scan on the given domain."""
    base_url = "http://localhost:8080"
    
    print(f"Ejecutando Spider para {domain}...")
    spider_response = requests.get(f"{base_url}/JSON/spider/action/scan/",
                                    params={"url": f"http://{domain}"})
    spider_id = spider_response.json().get("scan")
    
    while True:
        status = requests.get(f"{base_url}/JSON/spider/view/status/",
                              params={"scanId": spider_id}).json().get("status")
        if status == "100":
            break
        time.sleep(5)
    
    print(f"Spider completado para {domain}.")
    
    print(f"Ejecutando Active Scan para {domain}...")
    ascan_response = requests.get(f"{base_url}/JSON/ascan/action/scan/",
                                   params={"url": f"http://{domain}"})
    ascan_id = ascan_response.json().get("scan")
    
    while True:
        status = requests.get(f"{base_url}/JSON/ascan/view/status/",
                              params={"scanId": ascan_id}).json().get("status")
        if status == "100":
            break
        time.sleep(5)
    
    print(f"Active Scan completado para {domain}.")
    
    print(f"Generando informe para {domain}...")
    html_report = requests.get(f"{base_url}/OTHER/core/other/htmlreport/").text
    with open(f"owasp-zap-report-{domain}.html", "w") as file:
        file.write(html_report)
    print(f"Informe generado: owasp-zap-report-{domain}.html")

def main():
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("Uso:")
        print("  owaspzap-auto.py domain.com")
        print("  owaspzap-auto.py domain.com domain2.com")
        print("  owaspzap-auto.py --help")
        return
    
    domains = sys.argv[1:]
    
    try:
        install_requirements()
        start_owasp_zap()
        for domain in domains:
            perform_scan(domain)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        stop_owasp_zap()

if __name__ == "__main__":
    main()
