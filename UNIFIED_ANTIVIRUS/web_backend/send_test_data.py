"""
Script para enviar datos de prueba al backend de Vercel
"""
import requests
import json
from datetime import datetime
import uuid

API_BASE_URL = "https://unified-shield.vercel.app/api"
API_KEY = "5n8nAQro47O7bA8cjJXzHJxeTmKNQ9OcqRDurA1Xk4Y"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

print("🚀 Enviando datos de prueba al backend...")

# 1. Registrar instancias de prueba
instances = [
    {
        "id": str(uuid.uuid4()),
        "hostname": "PC-OFICINA-01",
        "os_info": "Windows 10 Pro",
        "antivirus_version": "1.1.0",
        "status": "active"
    },
    {
        "id": str(uuid.uuid4()),
        "hostname": "LAPTOP-VENTAS-02",
        "os_info": "Windows 11 Home",
        "antivirus_version": "1.1.0",
        "status": "active"
    },
    {
        "id": str(uuid.uuid4()),
        "hostname": "SERVER-BACKUP",
        "os_info": "Windows Server 2019",
        "antivirus_version": "1.0.9",
        "status": "inactive"
    }
]

print("\n📝 Registrando instancias...")
for instance in instances:
    response = requests.post(
        f"{API_BASE_URL}/instances",
        json=instance,
        headers=headers
    )
    if response.status_code in [200, 201]:
        print(f"✅ Instancia registrada: {instance['hostname']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

# 2. Enviar logs de prueba
print("\n📊 Enviando logs de prueba...")

logs = [
    {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "component": "scanner",
        "message": "Escaneo completado: 150 archivos analizados, 0 amenazas detectadas",
        "instance_id": instances[0]["id"],
        "details": {"files_scanned": 150, "threats_found": 0}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "component": "real_time_protection",
        "message": "Protección en tiempo real activada",
        "instance_id": instances[0]["id"],
        "details": {}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "level": "WARNING",
        "component": "behavior_detector",
        "message": "Proceso sospechoso detectado: chrome.exe intentando modificar registro",
        "instance_id": instances[1]["id"],
        "details": {"process": "chrome.exe", "action": "registry_modify"}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "component": "update_manager",
        "message": "Actualización de definiciones completada",
        "instance_id": instances[1]["id"],
        "details": {"version": "2025.11.29"}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "level": "ERROR",
        "component": "ml_detector",
        "message": "Error cargando modelo ONNX: archivo corrupto",
        "instance_id": instances[0]["id"],
        "details": {"error": "FileCorruptedException"}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "level": "WARNING",
        "component": "quarantine",
        "message": "Archivo movido a cuarentena: malware.exe",
        "instance_id": instances[1]["id"],
        "details": {"file": "C:\\Downloads\\malware.exe", "threat_type": "Trojan"}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "component": "scanner",
        "message": "Escaneo rápido iniciado",
        "instance_id": instances[1]["id"],
        "details": {}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "level": "ERROR",
        "component": "network_monitor",
        "message": "Conexión sospechosa bloqueada: 192.168.1.100:8080",
        "instance_id": instances[0]["id"],
        "details": {"ip": "192.168.1.100", "port": 8080}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "component": "system_health",
        "message": "Estado del sistema: OK",
        "instance_id": instances[1]["id"],
        "details": {"cpu": "15%", "memory": "45%"}
    },
    {
        "timestamp": datetime.now().isoformat(),
        "level": "WARNING",
        "component": "file_monitor",
        "message": "Archivo sospechoso detectado en descargas",
        "instance_id": instances[0]["id"],
        "details": {"file": "setup_crack.exe"}
    }
]

for log in logs:
    response = requests.post(
        f"{API_BASE_URL}/logs",
        json=log,
        headers=headers
    )
    if response.status_code in [200, 201]:
        print(f"✅ Log enviado: {log['level']} - {log['message'][:50]}...")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

print("\n🎉 ¡Datos de prueba enviados exitosamente!")
print(f"\n🌐 Abre el dashboard: https://unified-shield.vercel.app/dashboard.html")
print(f"   O localmente: file:///{__file__.replace('send_test_data.py', 'dashboard.html')}")
