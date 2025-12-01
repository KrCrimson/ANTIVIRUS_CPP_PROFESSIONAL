#!/usr/bin/env python3
"""
Script de prueba para activar específicamente el WebLogHandler
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.plugin_manager import PluginManager
from core.plugin_registry import PluginRegistry
from core.event_bus import event_bus

def test_web_log_handler():
    """Prueba específica del WebLogHandler"""
    
    # Crear instancias
    manager = PluginManager("plugins")
    
    print("🔍 Descubriendo plugins...")
    manager.discover_and_load_plugins()
    
    print("\n📋 Plugins encontrados:")
    for category, plugins in manager.registry._plugins.items():
        print(f"  {category}: {list(plugins.keys())}")
    
    print("\n🔧 Intentando activar web_log_handler...")
    success = manager.activate_plugin("web_log_handler")
    
    if success:
        print("✅ WebLogHandler activado exitosamente!")
        
        # Verificar suscripciones
        print("\n📡 Verificando suscripciones al EventBus:")
        print(f"  Suscriptores a 'security_alert': {len(event_bus._subscribers.get('security_alert', {}))}")
        
        # Probar publicar un evento
        print("\n🧪 Probando publicación de evento...")
        event_bus.publish('security_alert', {
            'threat_type': 'test',
            'process': 'test.exe',
            'pid': 1234,
            'detection_time': '2025-12-01T02:00:00',
            'severity': 'medium'
        }, 'test')
        
    else:
        print("❌ Error activando WebLogHandler")

if __name__ == "__main__":
    test_web_log_handler()