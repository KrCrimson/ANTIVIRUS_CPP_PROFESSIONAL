#!/usr/bin/env python3
"""
Script de prueba para enviar logs manualmente al servidor web
"""

import sys
import os
sys.path.append('utils')

from log_sender import LogSender
from datetime import datetime
import time

def test_log_sending():
    print("🧪 Iniciando prueba de envío de logs al servidor web...")
    
    # Crear instancia del log sender
    log_sender = LogSender('client_monitor_config.json')
    
    # Logs de prueba que simularían el antivirus
    test_logs = [
        {
            'timestamp': datetime.now().isoformat(),
            'level': 'INFO',
            'message': 'Protección iniciada - PRUEBA MANUAL',
            'extra_data': {
                'action': 'protection_start',
                'test': True,
                'component': 'manual_test'
            }
        },
        {
            'timestamp': datetime.now().isoformat(),
            'level': 'WARNING',
            'message': 'Amenaza detectada - SIMULACIÓN',
            'extra_data': {
                'action': 'threat_detected',
                'threat_type': 'keylogger_simulation',
                'process': 'test_malware.exe',
                'test': True
            }
        },
        {
            'timestamp': datetime.now().isoformat(),
            'level': 'ACTION', 
            'message': 'Proceso enviado a cuarentena - SIMULACIÓN',
            'extra_data': {
                'action': 'quarantine_completed',
                'process': 'test_malware.exe',
                'threat_type': 'keylogger_simulation',
                'test': True
            }
        }
    ]
    
    print(f"📊 Enviando {len(test_logs)} logs de prueba...")
    
    # Enviar logs
    for i, log in enumerate(test_logs, 1):
        print(f"📤 Enviando log {i}/{len(test_logs)}: {log['message']}")
        result = log_sender._send_logs_batch([log])
        
        if result:
            print("  ✅ Enviado exitosamente")
        else:
            print("  ❌ Error en envío")
        
        time.sleep(1)  # Esperar un poco entre envíos
    
    print("\n🎯 Prueba completada. Verifica el dashboard en: http://localhost:8888")
    print("🔍 También puedes ver la API en: http://localhost:8888/docs")

if __name__ == "__main__":
    # Cambiar al directorio correcto
    os.chdir(r"C:\Users\HP\Documents\GitHub\ANTIVIRUS_CPP_PROFESSIONAL\UNIFIED_ANTIVIRUS")
    
    test_log_sending()