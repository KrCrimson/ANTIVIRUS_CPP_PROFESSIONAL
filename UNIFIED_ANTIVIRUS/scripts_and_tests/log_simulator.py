#!/usr/bin/env python3
"""
Script para generar logs de prueba realistas y enviarlos al backend
para probar el dashboard con datos reales
"""

import json
import time
import random
import asyncio
import aiohttp
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.web_log_sender import WebLogSender

class AntivirusLogSimulator:
    def __init__(self, config_file="config/web_logging_optimized.json"):
        """Inicializar simulador de logs"""
        self.config_file = config_file
        self.load_config()
        self.sender = WebLogSender(self.web_config)
        
        # Plantillas de mensajes realistas
        self.log_templates = {
            'INFO': [
                "Sistema antivirus iniciado correctamente",
                "Escaneo programado completado sin amenazas",
                "Base de datos de definiciones actualizada",
                "Cuarentena aplicada exitosamente a {file}",
                "Conexión establecida con servidor de actualizaciones",
                "Monitor de archivos iniciado para {path}",
                "Plugin {plugin} cargado correctamente",
                "Verificación de integridad completada",
                "Respaldo de configuración creado"
            ],
            'WARNING': [
                "Archivo sospechoso detectado: {file}",
                "Comportamiento anómalo en proceso {process}",
                "Intento de conexión a IP conocida maliciosa: {ip}",
                "Modificación no autorizada detectada en {path}",
                "Plugin {plugin} respondiendo lentamente",
                "Memoria del sistema llegando al límite: {percent}%",
                "Archivo en lista gris encontrado: {file}",
                "Conexión de red sospechosa bloqueada",
                "Actividad de keylogger potencial detectada"
            ],
            'ERROR': [
                "Error crítico en motor de detección: {error}",
                "Fallo en conexión con servidor de actualizaciones",
                "No se pudo cargar plugin: {plugin}",
                "Acceso denegado al archivo de configuración",
                "Error de base de datos: {db_error}",
                "Memoria insuficiente para completar escaneo",
                "Plugin {plugin} ha dejado de responder",
                "Error en sistema de cuarentena",
                "Fallo en verificación de firma digital"
            ]
        }
        
        self.components = [
            'behavior_detector', 'ml_detector', 'network_detector',
            'file_monitor', 'process_monitor', 'network_monitor',
            'alert_manager', 'quarantine_handler', 'logger_handler'
        ]
        
        self.files = [
            'suspicious_file.exe', 'malware_sample.dll', 'keylogger.sys',
            'trojan_horse.bat', 'virus_payload.scr', 'rootkit_driver.sys',
            'adware_installer.exe', 'backdoor_tool.exe'
        ]
        
        self.processes = [
            'notepad.exe', 'chrome.exe', 'explorer.exe', 'system32.exe',
            'svchost.exe', 'winlogon.exe', 'unknown_process.exe'
        ]
        
        self.ips = [
            '192.168.1.100', '10.0.0.55', '172.16.1.99',
            '203.0.113.45', '198.51.100.22', '93.184.216.34'
        ]
        
        self.paths = [
            'C:\\Windows\\System32', 'C:\\Program Files',
            'C:\\Users\\Public', 'C:\\Temp', 'D:\\Downloads'
        ]
    
    def load_config(self):
        """Cargar configuración web logging"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.web_config = config.get('web_logging', {})
            print(f"✅ Configuración cargada desde {self.config_file}")
        except Exception as e:
            print(f"❌ Error cargando configuración: {e}")
            sys.exit(1)
    
    def generate_realistic_log(self):
        """Generar un log realista"""
        level = random.choices(
            ['INFO', 'WARNING', 'ERROR'],
            weights=[60, 35, 5]  # Distribución realista
        )[0]
        
        template = random.choice(self.log_templates[level])
        component = random.choice(self.components)
        
        # Sustituir placeholders
        message = template.format(
            file=random.choice(self.files),
            process=random.choice(self.processes),
            ip=random.choice(self.ips),
            path=random.choice(self.paths),
            plugin=random.choice(self.components),
            percent=random.randint(80, 95),
            error=f"Error {random.randint(1000, 9999)}",
            db_error=f"DB_ERR_{random.randint(100, 999)}"
        )
        
        # Generar timestamp realista (últimas 24 horas)
        now = datetime.now()
        hours_ago = random.uniform(0, 24)
        timestamp = now - timedelta(hours=hours_ago)
        
        return {
            'level': level,
            'message': message,
            'component': component,
            'timestamp': timestamp.isoformat(),
            'metadata': {
                'simulation': True,
                'batch_id': f"sim_{int(time.time())}",
                'source': 'log_simulator'
            }
        }
    
    async def simulate_batch_logs(self, count=50):
        """Simular envío de logs en lotes"""
        print(f"🔄 Generando {count} logs de prueba...")
        
        for i in range(count):
            log_entry = self.generate_realistic_log()
            
            try:
                self.sender.add_log(
                    timestamp=log_entry['timestamp'],
                    level=log_entry['level'],
                    logger='antivirus_simulator',
                    message=log_entry['message'],
                    component=log_entry['component'],
                    metadata=log_entry['metadata']
                )
                print(f"  ✅ Log {i+1}/{count}: {log_entry['level']} - {log_entry['message'][:60]}...")
                
                # Delay realista entre logs
                await asyncio.sleep(random.uniform(0.1, 0.5))
                
            except Exception as e:
                print(f"  ❌ Error enviando log {i+1}: {e}")
    
    async def simulate_realtime_stream(self, duration_minutes=5):
        """Simular stream de logs en tiempo real"""
        print(f"🚀 Iniciando simulación en tiempo real por {duration_minutes} minutos...")
        
        end_time = time.time() + (duration_minutes * 60)
        
        while time.time() < end_time:
            # Generar ráfagas de logs (simular actividad real)
            burst_size = random.randint(3, 12)
            
            for _ in range(burst_size):
                log_entry = self.generate_realistic_log()
                # Usar timestamp actual para tiempo real
                log_entry['timestamp'] = datetime.now().isoformat()
                
                try:
                    self.sender.add_log(
                        timestamp=log_entry['timestamp'],
                        level=log_entry['level'],
                        logger='antivirus_realtime',
                        message=log_entry['message'],
                        component=log_entry['component'],
                        metadata=log_entry['metadata']
                    )
                    print(f"📤 {log_entry['level']}: {log_entry['message'][:50]}...")
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            # Pausa entre ráfagas (actividad natural)
            await asyncio.sleep(random.uniform(5, 15))
        
        print("✅ Simulación en tiempo real completada")
    
    def cleanup(self):
        """Limpiar recursos"""
        try:
            if hasattr(self.sender, 'stop'):
                self.sender.stop()
            elif hasattr(self.sender, 'close'):
                self.sender.close()
        except Exception as e:
            print(f"⚠️ Warning durante cleanup: {e}")

async def main():
    """Función principal"""
    print("🧪 SIMULADOR DE LOGS ANTIVIRUS")
    print("=" * 50)
    
    simulator = AntivirusLogSimulator()
    
    try:
        print("\n1️⃣ Enviando lote inicial de logs históricos...")
        await simulator.simulate_batch_logs(100)
        
        print("\n2️⃣ Esperando envío automático de logs...")
        await asyncio.sleep(5)  # Dar tiempo para que se envíen los logs
        
        print("\n3️⃣ Iniciando simulación en tiempo real...")
        await simulator.simulate_realtime_stream(3)  # 3 minutos
        
        print("\n✅ Simulación completada!")
        print("🌐 Verifica el dashboard:")
        print("https://unified-antivirus-i1hdjk8ok-sebastians-projects-487d2baa.vercel.app")
        
    except KeyboardInterrupt:
        print("\n🛑 Simulación interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante simulación: {e}")
        import traceback
        traceback.print_exc()
    finally:
        simulator.cleanup()

if __name__ == "__main__":
    asyncio.run(main())