"""
Test Script para Web Log Sender
==============================

Script para probar el envío de logs al backend centralizado.
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from utils.web_log_sender import initialize_web_log_sender, send_web_log, shutdown_web_log_sender, get_web_sender_stats

# Datos de prueba
SAMPLE_COMPONENTS = [
    "core.engine", "core.plugin_manager", "core.event_bus",
    "plugins.behavior_detector", "plugins.ml_detector", "plugins.network_detector",
    "plugins.process_monitor", "plugins.file_monitor", "plugins.network_monitor",
    "plugins.alert_manager", "plugins.logger_handler", "plugins.quarantine_handler"
]

SAMPLE_MESSAGES = {
    "INFO": [
        "Sistema iniciado correctamente",
        "Plugin cargado exitosamente",
        "Escaneo completado sin amenazas",
        "Configuración actualizada",
        "Cache limpiado"
    ],
    "WARNING": [
        "Uso de memoria alto detectado",
        "Conexión de red lenta",
        "Archivo sospechoso encontrado",
        "Plugin tardando en responder",
        "Configuración no óptima detectada"
    ],
    "ERROR": [
        "Error al cargar plugin",
        "Fallo en la conexión a la base de datos",
        "Error de permisos al acceder archivo",
        "Timeout en análisis de red",
        "Error de validación de configuración"
    ],
    "CRITICAL": [
        "Amenaza crítica detectada y bloqueada",
        "Fallo crítico del motor principal",
        "Corrupción de datos detectada",
        "Intento de bypass de seguridad",
        "Sistema comprometido detectado"
    ]
}

async def generate_test_logs(duration_minutes: int = 5):
    """Generar logs de prueba durante un tiempo determinado"""
    print(f"🚀 Iniciando generación de logs de prueba por {duration_minutes} minutos...")
    
    # Inicializar web sender (cambiar URL por tu deployment de Vercel)
    await initialize_web_log_sender(
        api_endpoint="http://localhost:3000/api/logs",  # Cambiar en producción
        api_key="unified-antivirus-api-key-2024",
        client_id="test-client-001",
        antivirus_version="1.0.0-test"
    )
    
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration_minutes)
    log_count = 0
    
    try:
        while datetime.now() < end_time:
            # Generar log aleatorio
            level = random.choices(
                ["INFO", "WARNING", "ERROR", "CRITICAL"],
                weights=[60, 25, 12, 3],  # INFO más frecuente, CRITICAL raro
                k=1
            )[0]
            
            component = random.choice(SAMPLE_COMPONENTS)
            message = random.choice(SAMPLE_MESSAGES[level])
            
            # Metadatos adicionales
            metadata = {
                "test_run": True,
                "sequence": log_count,
                "cpu_usage": random.randint(10, 80),
                "memory_usage": random.randint(200, 1500)
            }
            
            # Añadir metadatos específicos según el nivel
            if level == "ERROR":
                metadata["error_code"] = random.randint(1000, 9999)
            elif level == "CRITICAL":
                metadata["threat_type"] = random.choice(["malware", "ransomware", "trojan", "rootkit"])
                metadata["confidence"] = random.uniform(0.8, 1.0)
            
            # Enviar log
            success = send_web_log(
                level=level,
                logger=f"test_logger_{component.split('.')[-1]}",
                message=message,
                component=component,
                metadata=metadata
            )
            
            if success:
                log_count += 1
                print(f"📝 [{level:8}] {component:25} | {message[:50]}...")
            else:
                print(f"❌ Error enviando log {log_count}")
            
            # Esperar intervalo variable (1-10 segundos)
            await asyncio.sleep(random.uniform(1, 10))
    
    except KeyboardInterrupt:
        print("\n⏹️ Detenido por usuario")
    
    # Mostrar estadísticas finales
    print(f"\n📊 Estadísticas finales:")
    print(f"   Logs generados: {log_count}")
    print(f"   Duración: {(datetime.now() - start_time).total_seconds():.1f} segundos")
    
    # Estadísticas del sender
    stats = get_web_sender_stats()
    if stats:
        print(f"   Logs enviados: {stats['total_sent']}")
        print(f"   Logs fallidos: {stats['total_failed']}")
        print(f"   Buffer actual: {stats['buffer_size']}")
        print(f"   Errores de conexión: {stats['connection_errors']}")
    
    # Esperar a que se envíen logs pendientes
    print("\n⏳ Esperando envío de logs pendientes...")
    await asyncio.sleep(35)
    
    # Estadísticas finales
    stats = get_web_sender_stats()
    if stats:
        print(f"📤 Estadísticas finales del sender:")
        print(f"   Total enviados: {stats['total_sent']}")
        print(f"   Total fallidos: {stats['total_failed']}")
        print(f"   Buffer restante: {stats['buffer_size']}")
    
    # Cerrar sender
    await shutdown_web_log_sender()
    print("✅ Test completado")

async def test_single_batch():
    """Enviar un batch único de logs para testing rápido"""
    print("🧪 Enviando batch único de logs de prueba...")
    
    await initialize_web_log_sender(
        api_endpoint="http://localhost:3000/api/logs",
        api_key="unified-antivirus-api-key-2024",
        client_id="test-batch-client",
        antivirus_version="1.0.0-batch-test"
    )
    
    # Enviar logs de diferentes niveles
    test_logs = [
        ("INFO", "core.engine", "Motor de antivirus iniciado correctamente"),
        ("INFO", "plugins.ml_detector", "Modelo ML cargado: keylogger_model_large.onnx"),
        ("WARNING", "plugins.behavior_detector", "Comportamiento sospechoso detectado en proceso explorer.exe"),
        ("ERROR", "plugins.network_monitor", "Timeout en análisis de paquete de red"),
        ("CRITICAL", "plugins.integration_engine", "Consenso de amenaza: MALWARE detectado con 95% confianza")
    ]
    
    for level, component, message in test_logs:
        metadata = {
            "batch_test": True,
            "timestamp": datetime.now().isoformat(),
            "pid": random.randint(1000, 9999),
            "confidence": random.uniform(0.5, 1.0) if level in ["WARNING", "ERROR", "CRITICAL"] else None
        }
        
        success = send_web_log(
            level=level,
            logger=f"batch_test_{component.split('.')[-1]}",
            message=message,
            component=component,
            metadata=metadata
        )
        
        print(f"{'✅' if success else '❌'} [{level:8}] {message}")
    
    # Esperar envío
    print("\n⏳ Esperando envío del batch...")
    await asyncio.sleep(35)
    
    # Mostrar estadísticas
    stats = get_web_sender_stats()
    if stats:
        print(f"📊 Resultados: {stats['total_sent']} enviados, {stats['total_failed']} fallidos")
    
    await shutdown_web_log_sender()
    print("✅ Batch test completado")

if __name__ == "__main__":
    print("🔧 UNIFIED_ANTIVIRUS - Test de Web Log Sender")
    print("=" * 50)
    
    mode = input("Seleccionar modo:\n1. Test continuo (5 min)\n2. Batch único\n3. Test personalizado\nOpción: ")
    
    if mode == "1":
        asyncio.run(generate_test_logs(5))
    elif mode == "2":
        asyncio.run(test_single_batch())
    elif mode == "3":
        minutes = int(input("Duración en minutos: "))
        asyncio.run(generate_test_logs(minutes))
    else:
        print("❌ Opción inválida")