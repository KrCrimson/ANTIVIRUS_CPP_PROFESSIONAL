"""
Web Log Handler Plugin - Sistema de envío de logs al backend web
==============================================================

Plugin handler que intercepta todos los logs del sistema antivirus
y los envía automáticamente al backend web para almacenamiento
persistente y visualización en tiempo real.

Características:
- Envío automático y buffereado de logs
- Reintento automático en caso de fallos de red
- Identificación única de instancia
- Registro automático de la instancia en el backend
- Soporte para diferentes tipos de eventos
- Estadísticas de envío y errores

Configuración:
- api_url: URL del backend web
- api_key: Clave de API para autenticación  
- batch_size: Número de logs por batch
- flush_interval: Intervalo de envío en segundos
- buffer_size: Tamaño máximo del buffer de logs

Autor: Sistema Antivirus Unificado
Versión: 1.0.0
"""

from .plugin import WebLogHandlerPlugin, create_plugin

__version__ = "1.0.0"
__author__ = "Sistema Antivirus Unificado"
__description__ = "Plugin para envío automático de logs al backend web"

__all__ = ["WebLogHandlerPlugin", "create_plugin"]