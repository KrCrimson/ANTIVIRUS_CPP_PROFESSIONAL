"""
Web System Integration Package
=============================

Paquete de integración del sistema de logging web con el antivirus core.
Proporciona handlers, configuración y utilidades para envío de logs al backend web.
"""

from .web_log_handler import WebLogHandler, create_web_log_handler
from .config_manager import (
    WebLogConfig, 
    WebLogConfigManager, 
    get_web_log_config,
    setup_web_logging_from_config
)

__version__ = "1.0.0"
__author__ = "Antivirus Team"

# Exportar componentes principales
__all__ = [
    'WebLogHandler',
    'create_web_log_handler',
    'WebLogConfig',
    'WebLogConfigManager', 
    'get_web_log_config',
    'setup_web_logging_from_config',
    'setup_antivirus_web_logging',
    'get_web_logging_status'
]


def setup_antivirus_web_logging(config_file: str = None, 
                               logger_names: list = None,
                               auto_enable: bool = True) -> dict:
    """
    Configuración rápida del sistema de logging web para el antivirus
    
    Args:
        config_file: Archivo de configuración (opcional)
        logger_names: Nombres de loggers a configurar (por defecto: loggers principales)
        auto_enable: Si habilitar automáticamente si la config es válida
        
    Returns:
        Dict con resultado de la configuración
    """
    import logging
    
    # Loggers por defecto del antivirus
    if logger_names is None:
        logger_names = [
            'antivirus_system',
            'core',
            'plugins', 
            'ml_detector',
            'behavior_detector',
            'network_detector',
            'file_monitor',
            'process_monitor',
            'network_monitor'
        ]
    
    result = {
        'success': False,
        'handler': None,
        'configured_loggers': [],
        'errors': [],
        'config': None
    }
    
    try:
        # Cargar configuración
        manager = WebLogConfigManager(config_file)
        config = manager.get_config()
        result['config'] = config.to_dict()
        
        # Validar configuración
        if not manager.validate_config():
            result['errors'].append("Configuración inválida")
            return result
        
        # Verificar si está habilitado
        if not config.enabled and not auto_enable:
            result['errors'].append("Web logging deshabilitado en configuración")
            return result
        
        # Test de conectividad
        if not manager.test_connection():
            result['errors'].append("No se pudo conectar al servidor web")
            if not auto_enable:
                return result
        
        # Crear handler
        handler = setup_web_logging_from_config(config_file)
        if not handler:
            result['errors'].append("No se pudo crear WebLogHandler")
            return result
        
        result['handler'] = handler
        
        # Configurar loggers
        for logger_name in logger_names:
            try:
                logger = logging.getLogger(logger_name)
                
                # Verificar si ya tiene WebLogHandler
                has_web_handler = any(
                    isinstance(h, WebLogHandler) for h in logger.handlers
                )
                
                if not has_web_handler:
                    logger.addHandler(handler)
                    result['configured_loggers'].append(logger_name)
                    
            except Exception as e:
                result['errors'].append(f"Error configurando logger '{logger_name}': {e}")
        
        result['success'] = len(result['configured_loggers']) > 0
        
        if result['success']:
            print(f"✅ Web logging configurado para {len(result['configured_loggers'])} loggers")
            print(f"🌐 Enviando logs a: {config.api_url}")
        
    except Exception as e:
        result['errors'].append(f"Error general: {e}")
    
    return result


def get_web_logging_status() -> dict:
    """
    Obtiene estado completo del sistema de logging web
    
    Returns:
        Dict con información de estado detallada
    """
    import logging
    
    status = {
        'timestamp': None,
        'config_status': {},
        'handlers_active': 0,
        'loggers_configured': [],
        'statistics': {},
        'connectivity': False,
        'errors': []
    }
    
    try:
        from datetime import datetime
        status['timestamp'] = datetime.now().isoformat()
        
        # Estado de configuración
        try:
            manager = WebLogConfigManager()
            status['config_status'] = manager.get_status()
            status['connectivity'] = manager.test_connection()
        except Exception as e:
            status['errors'].append(f"Error verificando configuración: {e}")
        
        # Buscar handlers activos
        try:
            root_logger = logging.getLogger()
            
            def find_web_handlers(logger):
                """Encuentra WebLogHandlers recursivamente"""
                handlers = []
                
                # Handlers del logger actual
                for handler in logger.handlers:
                    if isinstance(handler, WebLogHandler):
                        handlers.append({
                            'logger_name': logger.name,
                            'handler_id': id(handler),
                            'stats': handler.get_stats()
                        })
                
                # Handlers de loggers hijos
                for child_name, child_logger in logger.manager.loggerDict.items():
                    if isinstance(child_logger, logging.Logger):
                        handlers.extend(find_web_handlers(child_logger))
                
                return handlers
            
            web_handlers = find_web_handlers(root_logger)
            status['handlers_active'] = len(web_handlers)
            
            # Estadísticas agregadas
            if web_handlers:
                total_stats = {
                    'logs_sent': 0,
                    'logs_failed': 0,
                    'logs_buffered': 0,
                    'connected_handlers': 0
                }
                
                for handler_info in web_handlers:
                    stats = handler_info['stats']
                    total_stats['logs_sent'] += stats.get('logs_sent', 0)
                    total_stats['logs_failed'] += stats.get('logs_failed', 0)
                    total_stats['logs_buffered'] += stats.get('logs_buffered', 0)
                    
                    if stats.get('is_connected', False):
                        total_stats['connected_handlers'] += 1
                    
                    # Agregar logger a la lista
                    if handler_info['logger_name'] not in status['loggers_configured']:
                        status['loggers_configured'].append(handler_info['logger_name'])
                
                status['statistics'] = total_stats
                
        except Exception as e:
            status['errors'].append(f"Error verificando handlers: {e}")
    
    except Exception as e:
        status['errors'].append(f"Error general obteniendo estado: {e}")
    
    return status


def quick_setup(api_url: str = "http://localhost:8000/api",
                api_key: str = "antivirus-system-key-2024",
                level: str = "INFO") -> bool:
    """
    Configuración rápida para desarrollo/testing
    
    Args:
        api_url: URL del API
        api_key: API key
        level: Nivel de logging
        
    Returns:
        True si la configuración fue exitosa
    """
    try:
        # Crear configuración temporal
        config = WebLogConfig(
            api_url=api_url,
            api_key=api_key,
            level=level,
            enabled=True,
            buffer_size=100,  # Buffer pequeño para testing
            batch_size=5,
            flush_interval=2.0
        )
        
        # Validar
        errors = config.validate()
        if errors:
            print(f"❌ Errores de configuración: {errors}")
            return False
        
        # Crear handler
        handler = WebLogHandler(
            api_url=f"{config.api_url.rstrip('/')}/logs",
            api_key=config.api_key,
            buffer_size=config.buffer_size,
            batch_size=config.batch_size,
            flush_interval=config.flush_interval,
            level=getattr(logging, config.level.upper())
        )
        
        # Test de conexión
        if not handler.test_connection():
            print("⚠️ No se pudo conectar al servidor, pero handler configurado")
        
        # Agregar a logger root
        import logging
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        
        print(f"✅ Web logging configurado rápidamente: {api_url}")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración rápida: {e}")
        return False