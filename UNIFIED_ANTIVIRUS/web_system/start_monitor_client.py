"""
Script de inicio para el monitor de logs web
Ejecuta el envío automático de logs al backend Vercel usando la configuración y el client_id.
"""
import sys
import os
import time
from web_system.integration.web_log_handler import run_web_log_monitor

def main():
    # Puedes agregar argumentos si lo necesitas
    print("[Monitor] Iniciando monitor de logs web...")
    run_web_log_monitor()

if __name__ == "__main__":
    main()
