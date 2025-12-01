"""
Conversor de Logs a Formato Vercel
===================================

Este script lee los logs existentes del antivirus y los convierte
al formato esperado por el backend de Vercel, enviándolos automáticamente.
"""

import json
import os
import re
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Configuración
CONFIG_FILE = "client_monitor_config.json"
LOGS_DIR = Path("logs")

# Cargar configuración
def load_config():
    """Carga la configuración del cliente"""
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ No se encontró {CONFIG_FILE}")
        return None
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Obtener instance_id
def get_instance_id():
    """Obtiene el ID único de esta instancia"""
    try:
        from web_system.client_identity import ClientIdentity
        client = ClientIdentity()
        return client.instance_id
    except:
        import socket
        import uuid
        hostname = socket.gethostname()
        mac = hex(uuid.getnode())[2:]
        return f"{hostname}_{mac}"

# Parsear línea de log
def parse_log_line(line: str, source_file: str) -> Dict[str, Any]:
    """
    Convierte una línea de log al formato de Vercel
    
    Formatos soportados:
    - JSON: {"timestamp": "...", "level": "...", ...}
    - Texto: 2025-11-30 20:00:00 - logger_name - INFO - mensaje
    """
    line = line.strip()
    if not line:
        return None
    
    # Intentar parsear como JSON
    if line.startswith('{'):
        try:
            data = json.loads(line)
            return {
                'timestamp': data.get('timestamp', datetime.now().isoformat()),
                'level': data.get('level', 'INFO'),
                'message': data.get('message', ''),
                'component': data.get('logger', 'unknown'),
                'details': {
                    'source_file': source_file,
                    'raw_log': line
                }
            }
        except json.JSONDecodeError:
            pass
    
    # Parsear formato texto: timestamp - logger - level - message
    pattern = r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+-\s+(\S+)\s+-\s+(\w+)\s+-\s+(.+)$'
    match = re.match(pattern, line)
    
    if match:
        timestamp_str, logger, level, message = match.groups()
        return {
            'timestamp': timestamp_str.replace(' ', 'T'),
            'level': level,
            'message': message,
            'component': logger,
            'details': {
                'source_file': source_file
            }
        }
    
    # Si no coincide con ningún formato, crear entrada genérica
    return {
        'timestamp': datetime.now().isoformat(),
        'level': 'INFO',
        'message': line,
        'component': 'raw_log',
        'details': {
            'source_file': source_file,
            'raw_log': line
        }
    }

# Leer archivos de log
def read_log_files() -> List[Dict[str, Any]]:
    """Lee todos los archivos de log y los convierte"""
    logs = []
    
    # Buscar directorio de logs en la ubicación actual
    current_dir = Path.cwd()
    logs_dir = current_dir / "logs"
    
    if not logs_dir.exists():
        print(f"⚠️ Directorio de logs no encontrado: {logs_dir}")
        print(f"   Buscando en: {current_dir}")
        return logs
    
    # Archivos de log a procesar
    log_files = list(logs_dir.glob("*.log")) + list(logs_dir.glob("*.jsonl"))
    
    if not log_files:
        print(f"⚠️ No se encontraron archivos .log o .jsonl en {logs_dir}")
        return logs
    
    for log_file in log_files:
        print(f"📖 Leyendo {log_file.name}...")
        
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                line_count = 0
                for line in f:
                    parsed = parse_log_line(line, log_file.name)
                    if parsed:
                        logs.append(parsed)
                        line_count += 1
                
                print(f"   ✅ {line_count} líneas procesadas")
        except Exception as e:
            print(f"❌ Error leyendo {log_file.name}: {e}")
    
    return logs

# Enviar logs a Vercel
def send_logs_to_vercel(logs: List[Dict[str, Any]], config: Dict[str, Any], instance_id: str):
    """Envía los logs convertidos al backend de Vercel"""
    if not logs:
        print("ℹ️ No hay logs para enviar")
        return
    
    api_url = config['api_url']
    api_key = config['api_key']
    
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key
    }
    
    print(f"\n📤 Enviando {len(logs)} logs a Vercel...")
    
    success_count = 0
    error_count = 0
    
    for i, log in enumerate(logs, 1):
        # Agregar instance_id a cada log
        log['instance_id'] = instance_id
        
        try:
            response = requests.post(
                api_url,
                json=log,
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                success_count += 1
                if i % 10 == 0:
                    print(f"  ✅ {i}/{len(logs)} logs enviados...")
            else:
                error_count += 1
                print(f"  ❌ Error en log {i}: HTTP {response.status_code}")
        
        except Exception as e:
            error_count += 1
            print(f"  ❌ Error en log {i}: {e}")
    
    print(f"\n📊 Resumen:")
    print(f"  ✅ Exitosos: {success_count}")
    print(f"  ❌ Fallidos: {error_count}")
    print(f"  📈 Total: {len(logs)}")

# Registrar instancia
def register_instance(config: Dict[str, Any], instance_id: str):
    """Registra la instancia en el backend"""
    try:
        import socket
        import platform
        
        register_url = config['api_url'].replace('/logs', '/instances')
        
        instance_data = {
            "id": instance_id,
            "hostname": socket.gethostname(),
            "os_info": platform.platform(),
            "antivirus_version": "1.1.0",
            "status": "active"
        }
        
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': config['api_key']
        }
        
        response = requests.post(
            register_url,
            json=instance_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Instancia registrada: {instance_id}")
        else:
            print(f"⚠️ Error registrando instancia: {response.status_code}")
    
    except Exception as e:
        print(f"⚠️ No se pudo registrar la instancia: {e}")

# Main
def main():
    print("=" * 60)
    print("🔄 Conversor de Logs a Formato Vercel")
    print("=" * 60)
    
    # Cargar configuración
    config = load_config()
    if not config:
        return
    
    print(f"✅ Configuración cargada")
    print(f"   API URL: {config['api_url']}")
    
    # Obtener instance_id
    instance_id = get_instance_id()
    print(f"✅ Instance ID: {instance_id}")
    
    # Registrar instancia
    register_instance(config, instance_id)
    
    # Leer y convertir logs
    logs = read_log_files()
    print(f"✅ {len(logs)} logs leídos y convertidos")
    
    # Enviar a Vercel
    if logs:
        send_logs_to_vercel(logs, config, instance_id)
        print(f"\n🎉 ¡Proceso completado!")
        print(f"   Verifica el dashboard: https://unified-shield.vercel.app/dashboard")
    else:
        print("\n⚠️ No se encontraron logs para enviar")

if __name__ == "__main__":
    main()
