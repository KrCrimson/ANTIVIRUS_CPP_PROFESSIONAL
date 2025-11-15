"""
Cliente de Monitoreo Web - Script de inicio
==========================================

Este script inicia el cliente de envío de logs al servidor de monitoreo web.
"""

import json
import time
import sys
import os
from pathlib import Path

def main():
    """Función principal del cliente de monitoreo"""
    
    print("🔗 Iniciando cliente de monitoreo web del antivirus...")
    print()
    
    # Verificar archivo de configuración
    config_file = Path("client_monitor_config.json")
    if not config_file.exists():
        print("❌ Error: No se encuentra el archivo de configuración 'client_monitor_config.json'")
        print("💡 Ejecute primero: python setup_web_monitoring.py")
        return 1
    
    try:
        # Cargar configuración
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"🌐 Servidor destino: {config.get('server_url', 'No especificado')}")
        print(f"⏱️ Intervalo de envío: {config.get('send_interval', 30)} segundos")
        print(f"📦 Tamaño de lote: {config.get('batch_size', 100)} logs")
        print()
        
        # Importar log sender
        try:
            from utils.log_sender import LogSender
        except ImportError as e:
            print(f"❌ Error importando log_sender: {e}")
            print("💡 Verifique que el archivo utils/log_sender.py existe")
            return 1
        
        # Crear y configurar sender
        try:
            sender = LogSender(**config)
            print(f"🆔 PC ID: {sender.pc_id}")
            print(f"📊 Estado inicial: {sender.get_status()}")
            print()
        except Exception as e:
            print(f"❌ Error creando sender: {e}")
            return 1
        
        # Enviar log de prueba
        try:
            print("🧪 Enviando log de prueba...")
            success = sender.send_manual_log('INFO', 'Cliente de monitoreo iniciado correctamente')
            if success:
                print("✅ Log de prueba enviado exitosamente")
            else:
                print("⚠️ Log de prueba falló - verificar que el servidor esté ejecutándose")
                print(f"   URL servidor: {config.get('server_url')}")
        except Exception as e:
            error_msg = str(e)
            if "Connection" in error_msg or "timeout" in error_msg.lower():
                print("⚠️ No se puede conectar al servidor de monitoreo")
                print(f"   URL servidor: {config.get('server_url')}")
                print("   💡 Verifique que el servidor esté ejecutándose:")
                print("      python web_monitor_server.py")
            else:
                print(f"⚠️ Error en log de prueba: {e}")
            print("   🔄 El cliente continuará intentando en segundo plano...")
        
        print()
        
        # Iniciar servicio automático
        try:
            sender.start()
            print("🚀 Cliente de monitoreo iniciado correctamente")
            print("📡 Enviando logs automáticamente al servidor...")
            print("🔍 Presiona Ctrl+C para detener el cliente")
            print()
            
            # Bucle principal
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n⏹️ Deteniendo cliente de monitoreo...")
            
            try:
                sender.stop()
                print("✅ Cliente detenido correctamente")
            except Exception as e:
                print(f"⚠️ Error deteniendo cliente: {e}")
                
        except Exception as e:
            print(f"❌ Error en el cliente: {e}")
            return 1
            
    except json.JSONDecodeError as e:
        print(f"❌ Error en archivo de configuración: {e}")
        print("💡 Verifique que client_monitor_config.json tiene formato JSON válido")
        return 1
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        input("Presione Enter para salir...")
        sys.exit(1)