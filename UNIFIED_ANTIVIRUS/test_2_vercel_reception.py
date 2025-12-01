"""
Test 2: Verificar si Vercel está Recibiendo los Datos
======================================================

Este script verifica que el backend de Vercel está recibiendo y almacenando
los logs correctamente.
"""

import requests
import json
from datetime import datetime, timedelta

# Configuración
API_BASE_URL = "https://unified-shield.vercel.app/api"
API_KEY = "5n8nAQro47O7bA8cjJXzHJxeTmKNQ9OcqRDurA1Xk4Y"

def test_api_health():
    """Verifica que la API esté funcionando"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        
        if response.status_code == 200:
            print("✅ API de Vercel está funcionando")
            return True
        else:
            print(f"❌ API respondió con código: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Error conectando a la API: {e}")
        return False

def test_stats_endpoint():
    """Verifica el endpoint de estadísticas"""
    try:
        headers = {'X-API-Key': API_KEY}
        response = requests.get(f"{API_BASE_URL}/stats", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                stats = data.get('stats', {})
                
                print("\n📊 Estadísticas del backend:")
                print(f"   Total de logs: {stats.get('total_logs', 0)}")
                print(f"   Instancias activas: {stats.get('active_instances', 0)}")
                print(f"   Total de instancias: {stats.get('total_instances', 0)}")
                
                logs_by_level = stats.get('logs_by_level', {})
                if logs_by_level:
                    print(f"\n   Logs por nivel:")
                    for level, count in logs_by_level.items():
                        print(f"     {level}: {count}")
                
                return stats
            else:
                print("❌ Respuesta sin éxito")
                return None
        else:
            print(f"❌ Error obteniendo estadísticas: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_instances_endpoint():
    """Verifica las instancias registradas"""
    try:
        headers = {'X-API-Key': API_KEY}
        response = requests.get(f"{API_BASE_URL}/instances", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                instances = data.get('instances', [])
                
                print(f"\n🖥️ Instancias registradas: {len(instances)}")
                
                for i, instance in enumerate(instances, 1):
                    print(f"\n   Instancia {i}:")
                    print(f"     ID: {instance.get('id', 'N/A')[:16]}...")
                    print(f"     Hostname: {instance.get('hostname', 'N/A')}")
                    print(f"     OS: {instance.get('os_info', 'N/A')}")
                    print(f"     Estado: {instance.get('status', 'N/A')}")
                    
                    last_seen = instance.get('last_seen')
                    if last_seen:
                        try:
                            dt = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
                            print(f"     Última conexión: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                        except:
                            print(f"     Última conexión: {last_seen}")
                
                return instances
            else:
                print("❌ Respuesta sin éxito")
                return None
        else:
            print(f"❌ Error obteniendo instancias: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_logs_endpoint():
    """Verifica los logs recientes"""
    try:
        headers = {'X-API-Key': API_KEY}
        response = requests.get(
            f"{API_BASE_URL}/logs?limit=10", 
            headers=headers, 
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                logs = data.get('logs', [])
                
                print(f"\n📝 Logs recientes: {len(logs)}")
                
                if logs:
                    print("\n   Últimos 5 logs:")
                    for i, log in enumerate(logs[:5], 1):
                        timestamp = log.get('timestamp', 'N/A')
                        level = log.get('level', 'N/A')
                        message = log.get('message', 'N/A')
                        component = log.get('component', 'N/A')
                        
                        try:
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            time_str = dt.strftime('%H:%M:%S')
                        except:
                            time_str = timestamp
                        
                        print(f"\n   {i}. [{time_str}] {level}")
                        print(f"      Componente: {component}")
                        print(f"      Mensaje: {message[:60]}...")
                else:
                    print("   ⚠️ No hay logs en el sistema")
                
                return logs
            else:
                print("❌ Respuesta sin éxito")
                return None
        else:
            print(f"❌ Error obteniendo logs: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_send_log():
    """Envía un log de prueba para verificar que el endpoint funciona"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY
        }
        
        test_log = {
            'timestamp': datetime.now().isoformat(),
            'level': 'INFO',
            'message': 'Test log desde test_2_vercel_reception.py',
            'component': 'test_script',
            'instance_id': 'test_instance',
            'details': {
                'test': True
            }
        }
        
        response = requests.post(
            f"{API_BASE_URL}/logs",
            json=test_log,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print("\n✅ Log de prueba enviado exitosamente")
            return True
        else:
            print(f"\n❌ Error enviando log de prueba: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    
    except Exception as e:
        print(f"\n❌ Error enviando log de prueba: {e}")
        return False

def main():
    print("=" * 70)
    print("🌐 TEST 2: Verificación de Recepción en Vercel")
    print("=" * 70)
    
    # Test 1: Health check
    print("\n1️⃣ Verificando salud de la API...")
    api_ok = test_api_health()
    
    if not api_ok:
        print("\n❌ La API no está respondiendo. Verifica:")
        print("   - URL: https://unified-shield.vercel.app")
        print("   - Estado del deployment en Vercel")
        return
    
    # Test 2: Estadísticas
    print("\n2️⃣ Obteniendo estadísticas...")
    stats = test_stats_endpoint()
    
    # Test 3: Instancias
    print("\n3️⃣ Verificando instancias registradas...")
    instances = test_instances_endpoint()
    
    # Test 4: Logs
    print("\n4️⃣ Verificando logs recientes...")
    logs = test_logs_endpoint()
    
    # Test 5: Enviar log de prueba
    print("\n5️⃣ Enviando log de prueba...")
    send_ok = test_send_log()
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    
    checks = {
        "API funcionando": api_ok,
        "Estadísticas accesibles": stats is not None,
        "Instancias registradas": instances is not None and len(instances) > 0,
        "Logs presentes": logs is not None and len(logs) > 0,
        "Puede recibir logs": send_ok
    }
    
    for check, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check}")
    
    # Diagnóstico
    print("\n" + "=" * 70)
    print("🔧 DIAGNÓSTICO")
    print("=" * 70)
    
    if all(checks.values()):
        print("✅ Vercel está recibiendo datos correctamente")
        print("   El sistema de monitoreo está funcionando")
    else:
        if not checks["Instancias registradas"]:
            print("⚠️ No hay instancias registradas en Vercel")
            print("   - Verifica que el antivirus instalado esté corriendo")
            print("   - Ejecuta test_1_system_sending.py primero")
        
        if not checks["Logs presentes"]:
            print("⚠️ No hay logs en Vercel")
            print("   - El antivirus puede no estar enviando logs")
            print("   - Verifica la configuración en client_monitor_config.json")
            print("   - Ejecuta convert_logs_to_vercel.py para enviar logs existentes")
        
        if checks["Puede recibir logs"]:
            print("✅ El endpoint de logs funciona correctamente")
            print("   El problema está en el cliente, no en el servidor")
    
    print("\n🌐 Dashboard: https://unified-shield.vercel.app/dashboard")

if __name__ == "__main__":
    main()
