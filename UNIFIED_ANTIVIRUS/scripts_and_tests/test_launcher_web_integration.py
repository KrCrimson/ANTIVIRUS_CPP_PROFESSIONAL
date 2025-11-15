#!/usr/bin/env python3
"""
Test simple de integración con backend web desplegado
"""

import logging
import sys
import os
import time
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

def test_launcher_integration():
    """Test de integración del launcher con web logging"""
    
    print("🧪 TESTING LAUNCHER WEB LOGGING INTEGRATION")
    print("="*60)
    
    # Simular inicio del launcher con web logging
    print("🚀 Simulando inicio del antivirus con web logging...")
    
    try:
        # Importar y ejecutar la función setup_web_logging del launcher
        from launcher import setup_web_logging
        
        print("✅ Función setup_web_logging importada correctamente")
        
        # Ejecutar setup 
        print("🔧 Ejecutando setup_web_logging()...")
        setup_web_logging()
        print("✅ setup_web_logging() ejecutado sin errores")
        
        # Configurar un logger para probar
        logger = logging.getLogger('test_antivirus')
        
        # Enviar algunos logs de prueba
        print("\n📤 Enviando logs de prueba...")
        
        test_messages = [
            ("INFO", "🛡️ Sistema antivirus iniciado correctamente"),
            ("WARNING", "⚠️ Archivo sospechoso detectado: test_malware.exe"),
            ("ERROR", "❌ Conexión bloqueada a IP maliciosa: 192.168.1.100"),
            ("INFO", "✅ Cuarentena aplicada exitosamente"),
            ("WARNING", "🔍 Comportamiento anómalo detectado en proceso"),
        ]
        
        for level, message in test_messages:
            if level == "INFO":
                logger.info(message)
            elif level == "WARNING":
                logger.warning(message)
            elif level == "ERROR":
                logger.error(message)
            
            print(f"  📝 {level}: {message}")
            time.sleep(0.5)
        
        print("\n" + "="*60)
        print("✅ TEST COMPLETADO EXITOSAMENTE")
        print("📊 Verifica los logs en el dashboard:")
        print("🌐 https://unified-antivirus-csitvest3-sebastians-projects-487d2baa.vercel.app")
        print("="*60)
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando launcher: {e}")
        return False
    except Exception as e:
        print(f"❌ Error durante test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_launcher_integration()