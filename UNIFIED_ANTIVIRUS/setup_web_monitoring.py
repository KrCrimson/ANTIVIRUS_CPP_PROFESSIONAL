"""
Web Monitoring Setup - Configurador del sistema de monitoreo web
===============================================================

Este script configura e instala el sistema de monitoreo web para el antivirus.
Permite tanto configurar el cliente (PC con antivirus) como el servidor de monitoreo.
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, Any

# Configuración por defecto
DEFAULT_CONFIG = {
    "server": {
        "host": "0.0.0.0",
        "port": 8000,
        "admin_username": "admin",
        "admin_password": "antivirus2025",
        "database_path": "web_monitor.db"
    },
    "client": {
        "server_url": "http://localhost:8000",
        "send_interval": 30,
        "batch_size": 100,
        "max_retries": 3
    }
}

def install_dependencies():
    """Instala las dependencias necesarias"""
    print("📦 Instalando dependencias...")
    
    requirements = [
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0", 
        "pydantic>=2.4.2",
        "jinja2>=3.1.2",
        "python-multipart>=0.0.6",
        "aiofiles>=23.2.1",
        "pandas>=2.0.0",
        "requests>=2.31.0"
    ]
    
    for req in requirements:
        try:
            print(f"  Instalando {req}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Error instalando {req}: {e}")
            return False
    
    print("✅ Dependencias instaladas correctamente")
    return True

def create_config_file(config_path: str = "web_monitor_config.json"):
    """Crea archivo de configuración"""
    config_file = Path(config_path)
    
    if config_file.exists():
        print(f"⚠️ El archivo de configuración {config_path} ya existe")
        response = input("¿Desea sobrescribirlo? (y/N): ")
        if response.lower() != 'y':
            return str(config_file)
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Archivo de configuración creado: {config_path}")
    return str(config_file)

def setup_server(config: Dict[str, Any]):
    """Configura el servidor de monitoreo"""
    print("\n🖥️ CONFIGURANDO SERVIDOR DE MONITOREO")
    print("=" * 50)
    
    server_config = config["server"]
    
    # Verificar que existe el archivo del servidor
    server_file = Path("web_monitor_server.py")
    if not server_file.exists():
        print("❌ Error: No se encuentra web_monitor_server.py")
        return False
    
    # Crear directorio para templates si no existe
    templates_dir = Path("web_templates")
    if not templates_dir.exists():
        print("❌ Error: No se encuentra el directorio web_templates")
        return False
    
    # Crear directorio para archivos estáticos
    static_dir = Path("web_static")
    static_dir.mkdir(exist_ok=True)
    
    print(f"✅ Servidor configurado en puerto {server_config['port']}")
    print(f"✅ Usuario administrador: {server_config['admin_username']}")
    print(f"✅ Base de datos: {server_config['database_path']}")
    
    return True

def setup_client(config: Dict[str, Any]):
    """Configura el cliente de envío de logs"""
    print("\n💻 CONFIGURANDO CLIENTE DE ENVÍO")
    print("=" * 50)
    
    client_config = config["client"]
    
    # Verificar que existe el log sender
    sender_file = Path("utils/log_sender.py")
    if not sender_file.exists():
        print("❌ Error: No se encuentra utils/log_sender.py")
        return False
    
    # Crear configuración de cliente
    client_config_file = Path("client_monitor_config.json")
    with open(client_config_file, 'w', encoding='utf-8') as f:
        json.dump(client_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Cliente configurado para servidor: {client_config['server_url']}")
    print(f"✅ Intervalo de envío: {client_config['send_interval']} segundos")
    print(f"✅ Configuración guardada en: {client_config_file}")
    
    return True

def create_startup_scripts(config: Dict[str, Any]):
    """Crea scripts de inicio para servidor y cliente"""
    print("\n🚀 CREANDO SCRIPTS DE INICIO")
    print("=" * 40)
    
    # Script para iniciar el servidor
    server_script = """@echo off
echo Iniciando servidor de monitoreo web del antivirus...
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no está instalado o no está en PATH
    pause
    exit /b 1
)

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Iniciar servidor
echo Servidor disponible en: http://localhost:{port}
echo Dashboard: http://localhost:{port}
echo API Docs: http://localhost:{port}/docs
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python web_monitor_server.py

pause
""".format(port=config["server"]["port"])

    # Script para iniciar el cliente
    client_script = """@echo off
echo Iniciando cliente de monitoreo web del antivirus...
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no está instalado o no está en PATH
    pause
    exit /b 1
)

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Iniciar cliente
echo Enviando logs a: {server_url}
echo.
echo Presiona Ctrl+C para detener el cliente
echo.

python -c "
import json
from utils.log_sender import LogSender
import time

# Cargar configuración
with open('client_monitor_config.json', 'r') as f:
    config = json.load(f)

# Crear y configurar sender
sender = LogSender(**config)
print(f'PC ID: {{sender.pc_id}}')
print(f'Estado: {{sender.get_status()}}')

# Enviar log de prueba
sender.send_manual_log('INFO', 'Cliente de monitoreo iniciado')

# Iniciar servicio
sender.start()

try:
    print('Cliente iniciado. Presiona Ctrl+C para detener...')
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('\\nDeteniendo cliente...')
    sender.stop()
    print('Cliente detenido.')
"

pause
""".format(server_url=config["client"]["server_url"])

    # Escribir scripts
    with open("start_monitor_server.bat", 'w', encoding='utf-8') as f:
        f.write(server_script)
    
    with open("start_monitor_client.bat", 'w', encoding='utf-8') as f:
        f.write(client_script)
    
    print("✅ Script del servidor: start_monitor_server.bat")
    print("✅ Script del cliente: start_monitor_client.bat")

def create_integration_example():
    """Crea ejemplo de integración con el antivirus"""
    example_code = '''"""
Ejemplo de integración del monitoreo web con el antivirus
"""

from utils.logger import setup_web_monitoring, get_logger

def init_antivirus_with_monitoring():
    """Inicializa el antivirus con monitoreo web"""
    
    # Configurar logger principal
    logger = get_logger("antivirus_main")
    
    # Configurar monitoreo web (opcional)
    try:
        # Cargar configuración de cliente
        import json
        with open('client_monitor_config.json', 'r') as f:
            client_config = json.load(f)
        
        # Inicializar monitoreo web
        sender = setup_web_monitoring(**client_config)
        
        if sender:
            logger.info("✅ Monitoreo web configurado correctamente")
        else:
            logger.warning("⚠️ Monitoreo web no disponible")
            
    except Exception as e:
        logger.warning(f"⚠️ No se pudo configurar monitoreo web: {e}")
    
    # Continuar con inicialización normal del antivirus
    logger.info("🛡️ Antivirus iniciado")
    
    return logger

# Usar en el archivo principal del antivirus
if __name__ == "__main__":
    logger = init_antivirus_with_monitoring()
    
    # Tu código del antivirus aquí
    logger.info("Sistema antivirus en funcionamiento")
'''
    
    with open("integration_example.py", 'w', encoding='utf-8') as f:
        f.write(example_code)
    
    print("✅ Ejemplo de integración: integration_example.py")

def main():
    """Función principal del configurador"""
    parser = argparse.ArgumentParser(description="Configurador del sistema de monitoreo web")
    parser.add_argument("--mode", choices=["full", "server", "client"], 
                       default="full", help="Modo de configuración")
    parser.add_argument("--config", default="web_monitor_config.json",
                       help="Archivo de configuración")
    parser.add_argument("--no-install", action="store_true",
                       help="No instalar dependencias")
    
    args = parser.parse_args()
    
    print("🛡️ CONFIGURADOR DE MONITOREO WEB DEL ANTIVIRUS")
    print("=" * 55)
    print()
    
    # Instalar dependencias
    if not args.no_install:
        if not install_dependencies():
            print("❌ Error instalando dependencias")
            return 1
    
    # Crear/cargar configuración
    config_file = create_config_file(args.config)
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Error cargando configuración: {e}")
        return 1
    
    # Configurar según modo
    success = True
    
    if args.mode in ["full", "server"]:
        success &= setup_server(config)
    
    if args.mode in ["full", "client"]:
        success &= setup_client(config)
    
    if success and args.mode == "full":
        create_startup_scripts(config)
        create_integration_example()
        
        print("\n🎉 CONFIGURACIÓN COMPLETADA")
        print("=" * 30)
        print()
        print("📋 PRÓXIMOS PASOS:")
        print("1. Ejecutar 'start_monitor_server.bat' en el servidor")
        print("2. Ejecutar 'start_monitor_client.bat' en cada PC cliente")
        print("3. Acceder al dashboard: http://localhost:8000")
        print("4. Integrar con el antivirus usando 'integration_example.py'")
        print()
        print(f"👤 Usuario: {config['server']['admin_username']}")
        print(f"🔑 Contraseña: {config['server']['admin_password']}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())