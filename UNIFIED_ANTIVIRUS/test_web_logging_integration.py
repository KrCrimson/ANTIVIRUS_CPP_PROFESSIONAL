#!/usr/bin/env python3
"""
Test Script - Sistema de Web Logging del Antivirus
=================================================

Script de prueba para validar la integración entre el sistema de logging
del antivirus y el backend web FastAPI.
"""

import sys
import os
import time
from pathlib import Path

# Agregar el directorio del antivirus al path
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import (
    setup_web_logging, 
    enable_web_logging,
    test_web_logging_connection,
    get_web_logging_info,
    log_test_message,
    get_logger
)


def print_header(title: str):
    """Imprime un header decorado"""
    print("\n" + "="*60)
    print(f"🔧 {title}")
    print("="*60)


def print_status(status: dict):
    """Imprime estado de manera formateada"""
    print(f"📊 Estado del Web Logging:")
    print(f"  • Disponible: {'✅' if status.get('available', False) else '❌'}")
    print(f"  • Habilitado: {'✅' if status.get('enabled', False) else '❌'}")
    print(f"  • Conectividad: {'✅' if status.get('connectivity', False) else '❌'}")
    print(f"  • Handlers activos: {status.get('handlers_active', 0)}")
    print(f"  • Loggers configurados: {len(status.get('loggers_configured', []))}")
    
    if status.get('loggers_configured'):
        print(f"  • Loggers: {', '.join(status['loggers_configured'])}")
    
    if status.get('statistics'):
        stats = status['statistics']
        print(f"  • Logs enviados: {stats.get('logs_sent', 0)}")
        print(f"  • Logs fallidos: {stats.get('logs_failed', 0)}")
        print(f"  • Logs en buffer: {stats.get('logs_buffered', 0)}")
    
    if status.get('errors'):
        print(f"  ⚠️ Errores: {len(status['errors'])}")
        for error in status['errors']:
            print(f"     - {error}")


def test_web_logging_system():
    """Test completo del sistema de web logging"""
    
    print_header("INICIANDO TEST DEL SISTEMA DE WEB LOGGING")
    
    # 1. Verificar estado inicial
    print_header("1. VERIFICANDO ESTADO INICIAL")
    initial_status = get_web_logging_info()
    print_status(initial_status)
    
    # 2. Test de conectividad
    print_header("2. TEST DE CONECTIVIDAD")
    print("🔗 Probando conexión con el backend...")
    
    connection_ok = test_web_logging_connection()
    if connection_ok:
        print("✅ Conexión exitosa con el backend")
    else:
        print("❌ No se pudo conectar al backend")
        print("💡 Asegúrate de que el backend esté ejecutándose:")
        print("   cd web_system/backend && docker-compose up -d")
    
    # 3. Habilitar web logging
    print_header("3. HABILITANDO WEB LOGGING")
    
    if not initial_status.get('enabled', False):
        print("🔧 Habilitando web logging...")
        enable_result = enable_web_logging()
        
        if enable_result:
            print("✅ Web logging habilitado exitosamente")
        else:
            print("❌ Error habilitando web logging")
            return False
    else:
        print("ℹ️ Web logging ya estaba habilitado")
    
    # 4. Verificar configuración
    print_header("4. VERIFICANDO CONFIGURACIÓN")
    config_status = get_web_logging_info()
    print_status(config_status)
    
    # 5. Test de envío de logs
    print_header("5. TEST DE ENVÍO DE LOGS")
    
    if config_status.get('enabled', False):
        print("📤 Enviando logs de prueba...")
        
        # Test con diferentes niveles
        test_logs = [
            ("INFO", "Sistema de logging web funcionando correctamente"),
            ("WARNING", "Advertencia de prueba del sistema web"),
            ("ERROR", "Error simulado para testing del sistema"),
            ("DEBUG", "Información de debug para desarrollo")
        ]
        
        success_count = 0
        for level, message in test_logs:
            try:
                result = log_test_message(f"[TEST] {message}", level, "web_test")
                if result:
                    success_count += 1
                    print(f"  ✅ {level}: {message}")
                else:
                    print(f"  ❌ {level}: {message}")
            except Exception as e:
                print(f"  ❌ {level}: Error - {e}")
        
        print(f"\n📊 Enviados exitosamente: {success_count}/{len(test_logs)} logs")
        
        # Esperar un momento para el envío
        print("⏳ Esperando envío de logs...")
        time.sleep(3)
        
    else:
        print("❌ Web logging no está habilitado, saltando test de envío")
    
    # 6. Test de funcionalidad del antivirus
    print_header("6. TEST CON LOGGERS DEL ANTIVIRUS")
    
    # Obtener loggers del sistema antivirus
    antivirus_loggers = [
        "core",
        "plugins", 
        "ml_detector",
        "behavior_detector"
    ]
    
    print("🧪 Probando con loggers del antivirus...")
    
    for logger_name in antivirus_loggers:
        try:
            logger = get_logger(logger_name)
            logger.info(f"Test de {logger_name} - Web logging integrado", extra={
                'test_component': logger_name,
                'integration_test': True,
                'timestamp': time.time()
            })
            print(f"  ✅ Logger '{logger_name}' - OK")
        except Exception as e:
            print(f"  ❌ Logger '{logger_name}' - Error: {e}")
    
    # 7. Estado final
    print_header("7. ESTADO FINAL")
    final_status = get_web_logging_info()
    print_status(final_status)
    
    # 8. Resumen
    print_header("RESUMEN DEL TEST")
    
    success = (
        final_status.get('available', False) and
        final_status.get('enabled', False) and
        final_status.get('handlers_active', 0) > 0
    )
    
    if success:
        print("🎉 ¡TEST EXITOSO!")
        print("✅ El sistema de web logging está funcionando correctamente")
        print("📊 Los logs del antivirus se están enviando al backend web")
        print("🌐 Puedes ver los logs en: http://localhost:8000/docs")
    else:
        print("❌ TEST FALLIDO")
        print("🔧 Revisa la configuración y conectividad")
        
        if final_status.get('errors'):
            print("\n🐛 Errores encontrados:")
            for error in final_status['errors']:
                print(f"  - {error}")
    
    return success


def quick_demo():
    """Demo rápido del sistema"""
    print_header("DEMO RÁPIDO - WEB LOGGING")
    
    # Habilitar web logging
    print("🚀 Configurando web logging...")
    enable_web_logging()
    
    # Enviar algunos logs de demo
    print("📤 Enviando logs de demostración...")
    
    demo_logs = [
        ("INFO", "🛡️ Antivirus iniciado correctamente"),
        ("INFO", "🔍 Escaneando archivos del sistema"),
        ("WARNING", "⚠️ Archivo sospechoso detectado: malware.exe"),
        ("ERROR", "🚨 Amenaza bloqueada: Trojan.Generic.123"),
        ("INFO", "✅ Sistema protegido - 0 amenazas activas")
    ]
    
    for level, message in demo_logs:
        log_test_message(message, level, "antivirus_demo")
        time.sleep(1)  # Pausa dramática
    
    print("\n🎉 Demo completado!")
    print("🌐 Ve a http://localhost:8000/docs para ver los logs")
    print("📊 O usa: curl -H 'X-API-Key: antivirus-system-key-2024' http://localhost:8000/api/stats")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        quick_demo()
    else:
        test_web_logging_system()