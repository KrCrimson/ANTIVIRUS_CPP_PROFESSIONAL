#!/usr/bin/env python3
"""
Script simple para probar envío directo de logs
"""

import requests
import json
from datetime import datetime

def test_direct_log_send():
    """Prueba directa del envío de logs al servidor"""
    
    # Datos de prueba
    log_data = {
        "pc_id": "TEST_PC_MANUAL_123", 
        "timestamp": datetime.now().isoformat(),
        "logs": [
            {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "message": "PRUEBA MANUAL - Proteccion iniciada desde script directo",
                "extra_data": {
                    "action": "protection_start",
                    "test_manual": True,
                    "component": "direct_test_script"
                }
            },
            {
                "timestamp": datetime.now().isoformat(),
                "level": "WARNING",
                "message": "PRUEBA MANUAL - Amenaza detectada simulada",
                "extra_data": {
                    "action": "threat_detected",
                    "threat_type": "test_malware",
                    "process": "test_virus.exe",
                    "test_manual": True
                }
            }
        ]
    }
    
    try:
        print("Enviando logs de prueba al servidor...")
        print(f"URL: http://localhost:8888/api/recibir_logs")
        print(f"PC_ID: {log_data['pc_id']}")
        print(f"Logs a enviar: {len(log_data['logs'])}")
        
        # Enviar al servidor
        response = requests.post(
            "http://localhost:8888/api/recibir_logs",
            json=log_data,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nRespuesta del servidor:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Exito! Respuesta: {result}")
            print(f"Logs procesados: {result.get('logs_procesados', 'N/A')}")
        else:
            print(f"Error HTTP {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError as e:
        print("ERROR: No se pudo conectar al servidor.")
        print("Verifica que el servidor web este ejecutandose en puerto 8000")
        print(f"Detalles: {e}")
        
    except Exception as e:
        print(f"ERROR inesperado: {e}")
    
    print("Si el envio fue exitoso:")
    print("- Dashboard: http://localhost:8888")
    print("- API Docs: http://localhost:8888/docs")

if __name__ == "__main__":
    test_direct_log_send()