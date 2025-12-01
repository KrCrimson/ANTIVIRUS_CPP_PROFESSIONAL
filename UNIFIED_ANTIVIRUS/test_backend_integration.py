import requests
import json
import uuid
from datetime import datetime

# Configuración
API_URL = "https://unified-shield-le8n9y4ro-sebastians-projects-487d2baa.vercel.app"
API_KEY = "5n8nAQro47O7bA8cjJXzHJxeTmKNQ9OcqRDurA1Xk4Y"

def test_send_log():
    """Envía un log de prueba al backend"""
    
    # Generar ID único para esta sesión
    instance_id = f"test-client-{str(uuid.uuid4())[:8]}"
    
    # 1. Registrar la instancia
    instance_data = {
        "id": instance_id,
        "hostname": "TEST-PC",
        "os_info": "Windows 11 Pro", 
        "antivirus_version": "1.2.0",
        "status": "active"
    }
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    print("1. Registrando instancia...")
    try:
        response = requests.post(
            f"{API_URL}/api/instances",
            headers=headers,
            json=instance_data,
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"   Error registrando instancia: {e}")
        return
    
    # 2. Enviar varios logs de prueba
    test_logs = [
        {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "component": "CoreEngine", 
            "message": "Antivirus iniciado correctamente",
            "instance_id": instance_id,
            "details": {"startup_time": "2.3s"}
        },
        {
            "timestamp": datetime.now().isoformat(),
            "level": "WARNING",
            "component": "FileMonitor",
            "message": "[DETECTION] Proceso sospechoso detectado: suspicious_app.exe - patrón: keylogger",
            "instance_id": instance_id,
            "details": {"process": "suspicious_app.exe", "pattern": "keylogger", "risk_level": "medium"}
        },
        {
            "timestamp": datetime.now().isoformat(),
            "level": "ERROR",
            "component": "UpdateManager",
            "message": "Error actualizando base de datos de virus",
            "instance_id": instance_id,
            "details": {"error_code": "UPDATE_FAILED", "retry_count": 3}
        }
    ]
    
    print("\n2. Enviando logs de prueba...")
    for i, log_data in enumerate(test_logs, 1):
        try:
            response = requests.post(
                f"{API_URL}/api/logs",
                headers=headers,
                json=log_data,
                timeout=30
            )
            print(f"   Log {i}: Status {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"          Log ID: {result.get('log_id')}")
            else:
                print(f"          Error: {response.text}")
        except Exception as e:
            print(f"   Error enviando log {i}: {e}")
    
    print(f"\n✅ Prueba completada. Instance ID: {instance_id}")

if __name__ == "__main__":
    test_send_log()