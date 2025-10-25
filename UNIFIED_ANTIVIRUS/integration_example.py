"""
Ejemplo de integración del monitoreo web con el antivirus
"""

from utils.logger import setup_web_monitoring, get_logger

def init_antivirus_with_monitoring():
    """Inicializa el antivirus con monitoreo web"""
    
    # Configurar logger principal
    logger = get_logger("antivirus_main")
    
    # Configurar monitoreo web (opcional)
    try:
        # Cargar configuración de cliente
        import json
        with open('client_monitor_config.json', 'r') as f:
            client_config = json.load(f)
        
        # Inicializar monitoreo web
        sender = setup_web_monitoring(**client_config)
        
        if sender:
            logger.info("✅ Monitoreo web configurado correctamente")
        else:
            logger.warning("⚠️ Monitoreo web no disponible")
            
    except Exception as e:
        logger.warning(f"⚠️ No se pudo configurar monitoreo web: {e}")
    
    # Continuar con inicialización normal del antivirus
    logger.info("🛡️ Antivirus iniciado")
    
    return logger

# Usar en el archivo principal del antivirus
if __name__ == "__main__":
    logger = init_antivirus_with_monitoring()
    
    # Tu código del antivirus aquí
    logger.info("Sistema antivirus en funcionamiento")
