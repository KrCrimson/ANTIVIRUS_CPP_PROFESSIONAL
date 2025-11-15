#!/usr/bin/env python3
"""
Simulador de logs directo con requests HTTP para probar dashboard
"""

import requests
import json
import time
import random
from datetime import datetime, timedelta
import platform
import uuid

class DirectLogSender:
    def __init__(self):
        self.api_url = "https://unified-antivirus-duzz48bmm-sebastians-projects-487d2baa.vercel.app/api/logs"
        self.api_key = "unified-antivirus-api-key-2024"
        self.client_id = f"test-client-{uuid.uuid4().hex[:8]}"
        
        # Plantillas de mensajes realistas
        self.log_templates = {
            'INFO': [
                "🛡️ Sistema antivirus inicializado correctamente",
                "✅ Escaneo programado completado sin amenazas",
                "📡 Base de datos de definiciones actualizada",
                "🔒 Cuarentena aplicada exitosamente",
                "🔌 Plugin cargado correctamente",
                "📊 Verificación de integridad completada",
                "💾 Respaldo de configuración creado"
            ],
            'WARNING': [
                "⚠️ Archivo sospechoso detectado: malware_sample.exe",
                "🚨 Comportamiento anómalo en proceso notepad.exe",
                "🌐 Intento de conexión a IP maliciosa: 192.168.1.100",
                "📁 Modificación no autorizada detectada en C:\\Windows\\System32",
                "🐌 Plugin respondiendo lentamente",
                "💾 Memoria del sistema llegando al límite: 85%",
                "📄 Archivo en lista gris encontrado",
                "🔒 Conexión de red sospechosa bloqueada",
                "⌨️ Actividad de keylogger potencial detectada"
            ],
            'ERROR': [
                "❌ Error crítico en motor de detección",
                "🚫 Fallo en conexión con servidor de actualizaciones",
                "💥 No se pudo cargar plugin behavior_detector",
                "🔐 Acceso denegado al archivo de configuración",
                "💾 Error de base de datos: DB_ERR_404",
                "🆘 Memoria insuficiente para completar escaneo",
                "💀 Plugin ha dejado de responder",
                "🗂️ Error en sistema de cuarentena"
            ],
            'CRITICAL': [
                "🚨 AMENAZA CRÍTICA: Rootkit detectado en sistema",
                "💥 FALLO CRÍTICO: Motor principal no responde",
                "🔴 EMERGENCIA: Ataque en curso detectado",
                "⚠️ CRÍTICO: Sistema comprometido detectado"
            ]
        }
        
        self.components = [
            'behavior_detector', 'ml_detector', 'network_detector',
            'file_monitor', 'process_monitor', 'network_monitor',
            'alert_manager', 'quarantine_handler', 'logger_handler'
        ]
    
    def generate_realistic_log(self, custom_timestamp=None):
        """Generar log realista"""
        level = random.choices(
            ['INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            weights=[55, 30, 12, 3]
        )[0]
        
        message = random.choice(self.log_templates[level])
        component = random.choice(self.components)
        
        # Timestamp personalizado o reciente
        if custom_timestamp:
            timestamp = custom_timestamp
        else:
            now = datetime.now()
            hours_ago = random.uniform(0, 24)
            timestamp = now - timedelta(hours=hours_ago)
        
        return {
            "timestamp": timestamp.isoformat(),
            "level": level,
            "logger": "antivirus_core",
            "message": message,
            "component": component,
            "metadata": {
                "simulation": True,
                "test_batch": f"batch_{int(time.time())}",
                "source": "direct_simulator"
            }
        }
    
    def send_batch(self, logs_count=50):
        """Enviar lote de logs"""
        logs = []
        
        print(f"🔄 Generando {logs_count} logs de prueba...")
        
        for i in range(logs_count):
            log = self.generate_realistic_log()
            logs.append(log)
        
        # Payload para el API
        payload = {
            "clientId": self.client_id,
            "hostname": platform.node(),
            "version": "2.0.0-simulator",
            "os": f"{platform.system()} {platform.release()}",
            "logs": logs
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        
        print(f"📤 Enviando {logs_count} logs al backend...")
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Lote enviado exitosamente: {logs_count} logs")
                result = response.json()
                print(f"   📊 Procesados: {result.get('processed', 'N/A')}")
                return True
            else:
                print(f"❌ Error enviando lote: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    def simulate_realtime(self, duration_minutes=3):
        """Simular logs en tiempo real"""
        print(f"🚀 Iniciando simulación en tiempo real por {duration_minutes} minutos...")
        
        end_time = time.time() + (duration_minutes * 60)
        
        while time.time() < end_time:
            # Generar ráfaga pequeña de logs actuales
            current_logs = []
            burst_size = random.randint(2, 8)
            
            for _ in range(burst_size):
                log = self.generate_realistic_log(datetime.now())
                current_logs.append(log)
            
            # Enviar ráfaga
            payload = {
                "clientId": self.client_id,
                "hostname": platform.node(),
                "version": "2.0.0-realtime",
                "os": f"{platform.system()} {platform.release()}",
                "logs": current_logs
            }
            
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self.api_key
            }
            
            try:
                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=15
                )
                
                if response.status_code == 200:
                    for log in current_logs:
                        print(f"📤 {log['level']}: {log['message'][:60]}...")
                else:
                    print(f"⚠️ Error enviando ráfaga: {response.status_code}")
            
            except Exception as e:
                print(f"⚠️ Error temporal: {e}")
            
            # Pausa entre ráfagas
            time.sleep(random.uniform(3, 10))
        
        print("✅ Simulación en tiempo real completada")

def main():
    print("🧪 SIMULADOR DIRECTO DE LOGS")
    print("=" * 50)
    
    sender = DirectLogSender()
    
    try:
        print("\n1️⃣ Enviando logs históricos (últimas 24h)...")
        sender.send_batch(150)  # Lote grande para datos históricos
        
        print("\n2️⃣ Enviando segundo lote de logs...")
        sender.send_batch(100)
        
        print("\n3️⃣ Iniciando simulación en tiempo real...")
        sender.simulate_realtime(2)  # 2 minutos de logs en tiempo real
        
        print("\n✅ ¡Simulación completada!")
        print("🌐 Dashboard disponible en:")
        print("https://unified-antivirus-duzz48bmm-sebastians-projects-487d2baa.vercel.app")
        print("\n📊 Los gráficos deberían mostrar:")
        print("   • Estadísticas actualizadas")
        print("   • Logs por hora (últimas 24h)")
        print("   • Distribución por nivel (INFO, WARNING, ERROR)")
        print("   • Lista de logs recientes")
        
    except KeyboardInterrupt:
        print("\n🛑 Simulación interrumpida")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()