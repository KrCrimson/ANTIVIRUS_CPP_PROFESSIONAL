#!/usr/bin/env python3
"""
Script de prueba para verificar el envío de logs al backend de Vercel
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio actual al path para imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.web_log_sender import initialize_web_log_sender, send_web_log, get_web_sender_stats, shutdown_web_log_sender
import logging

# Configurar logging para ver los errores
logging.basicConfig(level=logging.DEBUG)

async def main():
    print("🧪 Iniciando prueba de envío de logs a Vercel...")
    
    try:
        # Inicializar el web sender
        sender = await initialize_web_log_sender(
            api_endpoint="https://unified-antivirus-api.vercel.app/api/logs",
            api_key="antivirus-key-2024-prod-12345",
            client_id=None,  # Se generará automáticamente
            antivirus_version="1.0.0-test"
        )
        
        print("✅ WebLogSender inicializado")
        
        # Enviar logs de prueba
        print("📤 Enviando logs de prueba...")
        
        send_web_log(
            level="INFO",
            logger="test_logger",
            message="Test message 1 - Prueba de conexión",
            component="test_component",
            metadata={"test": True, "source": "test_script"}
        )
        
        send_web_log(
            level="WARNING", 
            logger="behavior_detector",
            message="Test warning - Proceso sospechoso detectado: chrome.exe",
            component="behavior_detector",
            metadata={"process": "chrome.exe", "pattern": "capture"}
        )
        
        send_web_log(
            level="ERROR",
            logger="ml_detector", 
            message="Test error - Error cargando modelo ONNX",
            component="ml_detector",
            metadata={"model": "keylogger_model.onnx", "error_code": 404}
        )
        
        print("📤 Logs enviados al buffer")
        
        # Esperar a que se envíen (el intervalo es 30 segundos)
        print("⏳ Esperando envío automático (35 segundos)...")
        await asyncio.sleep(35)
        
        # Mostrar estadísticas
        stats = get_web_sender_stats()
        print("\n📊 Estadísticas finales:")
        print(f"  • Total enviados: {stats['total_sent']}")
        print(f"  • Total fallidos: {stats['total_failed']}")
        print(f"  • Errores de conexión: {stats['connection_errors']}")
        print(f"  • Buffer actual: {stats['buffer_size']}")
        print(f"  • Último envío: {stats['last_send']}")
        print(f"  • Cliente ID: {stats['client_id']}")
        
        # Cerrar
        await shutdown_web_log_sender()
        print("✅ Prueba completada")
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())