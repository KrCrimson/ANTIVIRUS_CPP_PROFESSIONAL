#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión del sistema de web logging
con el backend en Vercel.
"""

import sys
import asyncio
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.web_log_sender import initialize_web_log_sender, send_web_log, get_web_sender_stats
import time


async def test_connection():
    """Prueba la conexión con el backend"""
    print("🔍 Iniciando prueba de conexión con el backend...")
    print("=" * 60)
    
    # URL del backend en Vercel
    api_endpoint = "https://unified-antivirus-duzz48bmm-sebastians-projects-487d2baa.vercel.app/api/logs"
    api_key = "antivirus-key-2024-prod-12345"
    
    print(f"📡 Endpoint: {api_endpoint}")
    print(f"🔑 API Key: {api_key[:20]}...")
    print()
    
    try:
        # Inicializar el cliente
        print("1️⃣ Inicializando WebLogSender...")
        sender = await initialize_web_log_sender(
            api_endpoint=api_endpoint,
            api_key=api_key,
            antivirus_version="1.0.0-test"
        )
        print("   ✅ WebLogSender inicializado correctamente")
        print()
        
        # Enviar logs de prueba
        print("2️⃣ Enviando logs de prueba...")
        test_logs = [
            ("INFO", "test_connection", "Log de prueba 1 - Conexión exitosa", component="test"),
            ("WARNING", "test_connection", "Log de prueba 2 - Advertencia de prueba", component="test"),
            ("ERROR", "test_connection", "Log de prueba 3 - Error simulado", component="test"),
        ]
        
        for level, logger, message, component in test_logs:
            success = send_web_log(
                level=level,
                logger=logger,
                message=message,
                component=component,
                metadata={"test": True, "timestamp": time.time()}
            )
            if success:
                print(f"   ✅ Log {level} agregado al buffer")
            else:
                print(f"   ❌ Error agregando log {level}")
        
        print()
        print("3️⃣ Esperando envío de logs (35 segundos)...")
        print("   (Los logs se envían cada 30 segundos)")
        
        # Esperar a que se envíen los logs
        await asyncio.sleep(35)
        
        # Obtener estadísticas
        print()
        print("4️⃣ Obteniendo estadísticas...")
        stats = get_web_sender_stats()
        
        if stats:
            print(f"   📊 Estadísticas del cliente:")
            print(f"      - Client ID: {stats.get('client_id', 'N/A')}")
            print(f"      - Hostname: {stats.get('hostname', 'N/A')}")
            print(f"      - Logs enviados: {stats.get('total_sent', 0)}")
            print(f"      - Logs fallidos: {stats.get('total_failed', 0)}")
            print(f"      - Errores de conexión: {stats.get('connection_errors', 0)}")
            print(f"      - Buffer actual: {stats.get('buffer_size', 0)} logs")
            print(f"      - Estado: {'🟢 Activo' if stats.get('running', False) else '🔴 Inactivo'}")
            
            if stats.get('last_send'):
                print(f"      - Último envío: {stats.get('last_send')}")
            
            print()
            
            # Verificar si se enviaron logs
            if stats.get('total_sent', 0) > 0:
                print("✅ ¡ÉXITO! Los logs se enviaron correctamente al backend")
                print()
                print("📊 Verifica en el dashboard:")
                print(f"   https://unified-antivirus-duzz48bmm-sebastians-projects-487d2baa.vercel.app")
                print()
                print("   Busca logs con:")
                print("   - Logger: 'test_connection'")
                print("   - Component: 'test'")
                return True
            elif stats.get('connection_errors', 0) > 0:
                print("⚠️  ADVERTENCIA: Hubo errores de conexión")
                print("   Verifica:")
                print("   1. Que la URL del backend sea correcta")
                print("   2. Que el API key sea válido")
                print("   3. Que tengas conexión a internet")
                return False
            else:
                print("⏳ Los logs aún no se han enviado (puede tardar hasta 30 segundos)")
                print("   Ejecuta este script nuevamente en unos momentos")
                return None
        else:
            print("❌ No se pudieron obtener estadísticas")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cerrar el cliente
        print()
        print("5️⃣ Cerrando conexión...")
        from utils.web_log_sender import shutdown_web_log_sender
        await shutdown_web_log_sender()
        print("   ✅ Conexión cerrada")


if __name__ == "__main__":
    print("🧪 TEST DE CONEXIÓN - WEB LOGGING")
    print("=" * 60)
    print()
    
    result = asyncio.run(test_connection())
    
    print()
    print("=" * 60)
    if result is True:
        print("✅ PRUEBA EXITOSA")
        sys.exit(0)
    elif result is False:
        print("❌ PRUEBA FALLIDA")
        sys.exit(1)
    else:
        print("⏳ PRUEBA EN PROGRESO (ejecuta nuevamente)")
        sys.exit(0)

