"""
Test 1: Verificar si el Sistema Instalado está Enviando Logs
==============================================================

Este script verifica si el antivirus instalado está enviando logs al backend de Vercel.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta

# Rutas comunes de instalación
INSTALL_PATHS = [
    Path(r"C:\Program Files\AntivirusProfesional"),
    Path(r"C:\Program Files (x86)\AntivirusProfesional"),
    Path.home() / "AppData" / "Local" / "AntivirusProfesional"
]

def find_installation():
    """Encuentra la instalación del antivirus"""
    for path in INSTALL_PATHS:
        if path.exists():
            return path
    return None

def check_config(install_path):
    """Verifica la configuración del cliente"""
    config_file = install_path / "client_monitor_config.json"
    
    if not config_file.exists():
        print("❌ No se encontró client_monitor_config.json")
        return None
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print(f"✅ Configuración encontrada:")
    print(f"   API URL: {config.get('api_url')}")
    print(f"   Habilitado: {config.get('enabled')}")
    
    return config

def check_logs_directory(install_path):
    """Verifica el directorio de logs"""
    logs_dir = install_path / "logs"
    
    if not logs_dir.exists():
        print("⚠️ Directorio de logs no encontrado")
        return []
    
    log_files = list(logs_dir.glob("*.log")) + list(logs_dir.glob("*.jsonl"))
    
    print(f"\n📁 Archivos de log encontrados: {len(log_files)}")
    
    recent_logs = []
    cutoff_time = datetime.now() - timedelta(minutes=30)
    
    for log_file in log_files:
        mod_time = datetime.fromtimestamp(log_file.stat().st_mtime)
        if mod_time > cutoff_time:
            recent_logs.append((log_file, mod_time))
            print(f"   ✅ {log_file.name} (modificado: {mod_time.strftime('%H:%M:%S')})")
    
    return recent_logs

def check_web_system(install_path):
    """Verifica el sistema de monitoreo web"""
    web_system = install_path / "web_system"
    
    if not web_system.exists():
        print("❌ Sistema web_system no encontrado")
        return False
    
    client_identity = web_system / "client_identity.py"
    web_log_handler = web_system / "integration" / "web_log_handler.py"
    
    print(f"\n🔍 Componentes del sistema web:")
    print(f"   {'✅' if client_identity.exists() else '❌'} client_identity.py")
    print(f"   {'✅' if web_log_handler.exists() else '❌'} web_log_handler.py")
    
    return client_identity.exists() and web_log_handler.exists()

def check_running_process():
    """Verifica si el proceso del antivirus está corriendo"""
    try:
        import psutil
        
        for proc in psutil.process_iter(['name', 'exe']):
            if 'professional_ui_robust' in proc.info['name'].lower():
                print(f"\n✅ Proceso encontrado:")
                print(f"   PID: {proc.pid}")
                print(f"   Nombre: {proc.info['name']}")
                print(f"   Ejecutable: {proc.info['exe']}")
                return True
        
        print("\n⚠️ Proceso del antivirus no encontrado")
        return False
    
    except ImportError:
        print("\n⚠️ psutil no disponible, no se puede verificar el proceso")
        return None

def check_fallback_logs(install_path):
    """Verifica si hay logs de fallback (indica problemas de conexión)"""
    fallback_file = install_path / "logs" / "web_log_fallback.log"
    
    if fallback_file.exists():
        size = fallback_file.stat().st_size
        mod_time = datetime.fromtimestamp(fallback_file.stat().st_mtime)
        
        print(f"\n⚠️ Archivo de fallback encontrado:")
        print(f"   Tamaño: {size} bytes")
        print(f"   Última modificación: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Esto indica que hubo problemas enviando logs al servidor")
        
        return True
    
    return False

def main():
    print("=" * 70)
    print("🔍 TEST 1: Verificación del Sistema Instalado")
    print("=" * 70)
    
    # Buscar instalación
    print("\n1️⃣ Buscando instalación del antivirus...")
    install_path = find_installation()
    
    if not install_path:
        print("❌ No se encontró la instalación del antivirus")
        print("\nVerifica que el antivirus esté instalado en una de estas rutas:")
        for path in INSTALL_PATHS:
            print(f"   - {path}")
        return
    
    print(f"✅ Instalación encontrada en: {install_path}")
    
    # Verificar configuración
    print("\n2️⃣ Verificando configuración...")
    config = check_config(install_path)
    
    # Verificar sistema web
    print("\n3️⃣ Verificando componentes del sistema web...")
    web_ok = check_web_system(install_path)
    
    # Verificar proceso
    print("\n4️⃣ Verificando proceso del antivirus...")
    process_running = check_running_process()
    
    # Verificar logs
    print("\n5️⃣ Verificando logs recientes (últimos 30 minutos)...")
    recent_logs = check_logs_directory(install_path)
    
    # Verificar fallback
    print("\n6️⃣ Verificando logs de fallback...")
    has_fallback = check_fallback_logs(install_path)
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    
    checks = {
        "Instalación encontrada": install_path is not None,
        "Configuración válida": config is not None,
        "Componentes web presentes": web_ok,
        "Proceso corriendo": process_running,
        "Logs recientes generados": len(recent_logs) > 0,
        "Sin problemas de conexión": not has_fallback
    }
    
    for check, status in checks.items():
        icon = "✅" if status else "❌" if status is False else "⚠️"
        print(f"{icon} {check}")
    
    # Diagnóstico
    print("\n" + "=" * 70)
    print("🔧 DIAGNÓSTICO")
    print("=" * 70)
    
    if all(v for v in checks.values() if v is not None):
        print("✅ El sistema parece estar funcionando correctamente")
        print("   Los logs deberían estar llegando a Vercel")
    else:
        print("⚠️ Se detectaron algunos problemas:")
        
        if not checks["Proceso corriendo"]:
            print("   - El antivirus no está corriendo. Inícialo primero.")
        
        if not checks["Logs recientes generados"]:
            print("   - No se han generado logs recientes.")
            print("     Deja el antivirus correr unos minutos.")
        
        if has_fallback:
            print("   - Hay logs de fallback, indica problemas de conexión.")
            print("     Verifica la configuración de red y la API key.")
    
    print("\n💡 Siguiente paso: Ejecuta test_2_vercel_reception.py para verificar")
    print("   que Vercel está recibiendo los datos correctamente.")

if __name__ == "__main__":
    main()
