"""
Script directo para enviar logs desde la instalación a Vercel
"""
import requests
import json
import re
from datetime import datetime
from pathlib import Path

# Configuración
API_URL = "https://unified-shield.vercel.app/api/logs"
API_KEY = "5n8nAQro47O7bA8cjJXzHJxeTmKNQ9OcqRDurA1Xk4Y"
INSTANCE_ID = "R3DCR0WN_155d528240"
LOGS_DIR = Path(r"C:\Program Files\AntivirusProfesional\logs")

headers = {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY
}

def parse_log_line(line, source_file):
    """Parsea una línea de log"""
    line = line.strip()
    if not line:
        return None
    
    # Formato: 2025-11-30 21:45:08,621 - logger - LEVEL - message
    pattern = r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}),\d+\s+-\s+(.+?)\s+-\s+(\w+)\s+-\s+(.+)$'
    match = re.match(pattern, line)
    
    if match:
        timestamp_str, logger, level, message = match.groups()
        return {
            'timestamp': timestamp_str.replace(' ', 'T'),
            'level': level,
            'message': message,
            'component': logger,
            'instance_id': INSTANCE_ID,
            'details': {'source_file': source_file}
        }
    
    return {
        'timestamp': datetime.now().isoformat(),
        'level': 'INFO',
        'message': line,
        'component': 'raw_log',
        'instance_id': INSTANCE_ID,
        'details': {'source_file': source_file}
    }

print("=" * 60)
print("📤 Enviando logs a Vercel")
print("=" * 60)

# Leer todos los archivos .log
log_files = list(LOGS_DIR.glob("*.log"))
print(f"\n📁 Archivos encontrados: {len(log_files)}")

total_sent = 0
total_errors = 0

for log_file in log_files:
    print(f"\n📖 Procesando {log_file.name}...")
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            print(f"   {len(lines)} líneas encontradas")
            
            sent = 0
            for line in lines:
                log_data = parse_log_line(line, log_file.name)
                if log_data:
                    try:
                        response = requests.post(API_URL, json=log_data, headers=headers, timeout=5)
                        if response.status_code in [200, 201]:
                            sent += 1
                        else:
                            total_errors += 1
                    except:
                        total_errors += 1
            
            print(f"   ✅ {sent} logs enviados")
            total_sent += sent
    
    except Exception as e:
        print(f"   ❌ Error: {e}")

print(f"\n" + "=" * 60)
print(f"📊 RESUMEN")
print(f"=" * 60)
print(f"✅ Total enviados: {total_sent}")
print(f"❌ Total errores: {total_errors}")
print(f"\n🌐 Verifica el dashboard:")
print(f"   https://unified-shield.vercel.app/dashboard")
