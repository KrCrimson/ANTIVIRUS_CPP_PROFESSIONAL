"""
Web Logging Configuration Manager
================================

Administrador de configuración para integración web del sistema de logging.
Maneja configuración, validación y inicialización del WebLogHandler.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .web_log_handler import WebLogHandler
from dataclasses import dataclass, asdict
import logging


@dataclass
class WebLogConfig:
    """Configuración para WebLogHandler"""
    
    # API Configuration
    api_url: str = "http://localhost:8000/api"
    api_key: str = "antivirus-system-key-2024"
    
    # Buffer Configuration  
    buffer_size: int = 1000
    batch_size: int = 10
    flush_interval: float = 5.0
    
    # Connection Configuration
    max_retries: int = 3
    timeout: float = 10.0
    connection_test_interval: float = 60.0  # seconds
    
    # Fallback Configuration
    fallback_file: Optional[str] = "logs/web_fallback.log"
    fallback_enabled: bool = True
    
    # Logging Configuration
    level: str = "INFO"
    enabled: bool = False
    
    # Advanced Options
    compress_logs: bool = False
    include_system_info: bool = True
    rate_limit_per_minute: int = 1000
    
    # Security
    verify_ssl: bool = True
    ca_cert_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la configuración a diccionario"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WebLogConfig':
        """Crea configuración desde diccionario"""
        # Filtrar solo campos válidos
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)
    
    def validate(self) -> List[str]:
        """
        Valida la configuración
        
        Returns:
            Lista de errores de validación (vacía si es válida)
        """
        errors = []
        
        # Validar URL
        if not self.api_url or not isinstance(self.api_url, str):
            errors.append("api_url debe ser una URL válida")
        elif not (self.api_url.startswith('http://') or self.api_url.startswith('https://')):
            errors.append("api_url debe comenzar con http:// o https://")
        
        # Validar API key
        if not self.api_key or len(self.api_key) < 8:
            errors.append("api_key debe tener al menos 8 caracteres")
        
        # Validar buffer
        if self.buffer_size <= 0 or self.buffer_size > 100000:
            errors.append("buffer_size debe estar entre 1 y 100000")
        
        if self.batch_size <= 0 or self.batch_size > self.buffer_size:
            errors.append("batch_size debe estar entre 1 y buffer_size")
        
        # Validar timeouts
        if self.flush_interval <= 0 or self.flush_interval > 300:
            errors.append("flush_interval debe estar entre 0.1 y 300 segundos")
        
        if self.timeout <= 0 or self.timeout > 120:
            errors.append("timeout debe estar entre 0.1 y 120 segundos")
        
        # Validar retries
        if self.max_retries < 0 or self.max_retries > 10:
            errors.append("max_retries debe estar entre 0 y 10")
        
        # Validar nivel de logging
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.level.upper() not in valid_levels:
            errors.append(f"level debe ser uno de: {valid_levels}")
        
        # Validar rate limit
        if self.rate_limit_per_minute <= 0 or self.rate_limit_per_minute > 100000:
            errors.append("rate_limit_per_minute debe estar entre 1 y 100000")
        
        return errors


class WebLogConfigManager:
    """
    Administrador de configuración para el sistema de logging web
    """
    
    DEFAULT_CONFIG_FILE = "config/web_logging_config.json"
    
    def __init__(self, config_file: str = None):
        """
        Inicializa el manager de configuración
        
        Args:
            config_file: Ruta al archivo de configuración
        """
        self.config_file = Path(config_file or self.DEFAULT_CONFIG_FILE)
        self.config = WebLogConfig()
        self._load_config()
    
    def _load_config(self):
        """Carga configuración desde archivo"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extraer configuración web logging si está anidada
                web_config = data.get('web_logging', data)
                self.config = WebLogConfig.from_dict(web_config)
                
                print(f"✅ Configuración web logging cargada desde {self.config_file}")
            else:
                print(f"⚠️ Archivo de configuración no encontrado: {self.config_file}")
                print("📝 Usando configuración por defecto")
                self._save_default_config()
                
        except Exception as e:
            print(f"❌ Error cargando configuración: {e}")
            print("📝 Usando configuración por defecto")
    
    def _save_default_config(self):
        """Guarda configuración por defecto"""
        try:
            # Crear directorio si no existe
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Configuración completa con comentarios
            config_data = {
                "_comment": "Configuración del sistema de logging web del antivirus",
                "_version": "1.0.0",
                "_last_updated": "2025-11-07",
                
                "web_logging": {
                    "_description": "Configuración para envío de logs al servidor web",
                    
                    "enabled": False,
                    "_enabled_comment": "Habilitar/deshabilitar envío de logs al servidor web",
                    
                    "api_url": "http://localhost:8000/api",
                    "_api_url_comment": "URL base del API del servidor de logs",
                    
                    "api_key": "antivirus-system-key-2024",
                    "_api_key_comment": "Clave API para autenticación",
                    
                    "level": "INFO",
                    "_level_comment": "Nivel mínimo de logs a enviar (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
                    
                    "buffer_size": 1000,
                    "_buffer_size_comment": "Tamaño máximo del buffer local de logs",
                    
                    "batch_size": 10,
                    "_batch_size_comment": "Número de logs a enviar por lote",
                    
                    "flush_interval": 5.0,
                    "_flush_interval_comment": "Intervalo en segundos para envío automático",
                    
                    "max_retries": 3,
                    "_max_retries_comment": "Número máximo de reintentos por envío",
                    
                    "timeout": 10.0,
                    "_timeout_comment": "Timeout en segundos para requests HTTP",
                    
                    "connection_test_interval": 60.0,
                    "_connection_test_interval_comment": "Intervalo para test de conectividad",
                    
                    "fallback_enabled": True,
                    "fallback_file": "logs/web_fallback.log",
                    "_fallback_comment": "Archivo de respaldo cuando falla el envío web",
                    
                    "compress_logs": False,
                    "_compress_comment": "Comprimir logs antes de enviar (reduce ancho de banda)",
                    
                    "include_system_info": True,
                    "_system_info_comment": "Incluir información del sistema en logs",
                    
                    "rate_limit_per_minute": 1000,
                    "_rate_limit_comment": "Límite de logs por minuto",
                    
                    "verify_ssl": True,
                    "ca_cert_path": None,
                    "_ssl_comment": "Configuración SSL para conexiones HTTPS"
                },
                
                "_examples": {
                    "development": {
                        "api_url": "http://localhost:8000/api",
                        "enabled": True,
                        "level": "DEBUG"
                    },
                    "production": {
                        "api_url": "https://logs.empresa.com/api",
                        "enabled": True,
                        "level": "WARNING",
                        "verify_ssl": True,
                        "compress_logs": True
                    },
                    "enterprise": {
                        "api_url": "https://siem.empresa.com/api/antivirus",
                        "api_key": "production-key-secure",
                        "enabled": True,
                        "level": "INFO",
                        "buffer_size": 5000,
                        "batch_size": 50,
                        "rate_limit_per_minute": 5000
                    }
                }
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            print(f"📝 Configuración por defecto guardada en {self.config_file}")
            
        except Exception as e:
            print(f"❌ Error guardando configuración por defecto: {e}")
    
    def save_config(self):
        """Guarda configuración actual"""
        try:
            # Cargar configuración existente para preservar comentarios
            existing_data = {}
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            
            # Actualizar solo la sección web_logging
            existing_data['web_logging'] = self.config.to_dict()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuración guardada en {self.config_file}")
            
        except Exception as e:
            print(f"❌ Error guardando configuración: {e}")
    
    def get_config(self) -> WebLogConfig:
        """Obtiene configuración actual"""
        return self.config
    
    def update_config(self, **kwargs):
        """
        Actualiza configuración
        
        Args:
            **kwargs: Parámetros a actualizar
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
            else:
                print(f"⚠️ Parámetro desconocido: {key}")
    
    def validate_config(self) -> bool:
        """
        Valida configuración actual
        
        Returns:
            True si la configuración es válida
        """
        errors = self.config.validate()
        
        if errors:
            print("❌ Errores de configuración:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        print("✅ Configuración válida")
        return True
    
    def enable_web_logging(self, api_url: str = None, api_key: str = None):
        """
        Habilita logging web con configuración opcional
        
        Args:
            api_url: URL del API (opcional)
            api_key: API key (opcional)
        """
        if api_url:
            self.config.api_url = api_url
        if api_key:
            self.config.api_key = api_key
        
        self.config.enabled = True
        
        if self.validate_config():
            self.save_config()
            print("✅ Web logging habilitado")
        else:
            self.config.enabled = False
            print("❌ No se pudo habilitar web logging debido a errores de configuración")
    
    def disable_web_logging(self):
        """Deshabilita logging web"""
        self.config.enabled = False
        self.save_config()
        print("🔒 Web logging deshabilitado")
    
    def test_connection(self) -> bool:
        """
        Test de conectividad con el servidor
        
        Returns:
            True si la conexión es exitosa
        """
        try:
            import requests
            
            # Test endpoint de health
            health_url = f"{self.config.api_url.rstrip('/')}/health"
            
            response = requests.get(
                health_url,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            
            success = response.status_code == 200
            
            if success:
                print(f"✅ Conexión exitosa con {health_url}")
                return True
            else:
                print(f"❌ Error de conexión: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error de conectividad: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtiene estado actual del sistema
        
        Returns:
            Dict con información de estado
        """
        return {
            'enabled': self.config.enabled,
            'api_url': self.config.api_url,
            'level': self.config.level,
            'config_file': str(self.config_file),
            'config_exists': self.config_file.exists(),
            'valid_config': len(self.config.validate()) == 0,
            'buffer_size': self.config.buffer_size,
            'batch_size': self.config.batch_size,
            'fallback_enabled': self.config.fallback_enabled
        }


# =================== CONVENIENCE FUNCTIONS ===================
def get_web_log_config(config_file: str = None) -> WebLogConfig:
    """
    Función de conveniencia para obtener configuración
    
    Args:
        config_file: Archivo de configuración (opcional)
        
    Returns:
        Configuración de web logging
    """
    manager = WebLogConfigManager(config_file)
    return manager.get_config()


def setup_web_logging_from_config(config_file: str = None) -> Optional['WebLogHandler']:
    """
    Configura WebLogHandler desde archivo de configuración
    
    Args:
        config_file: Archivo de configuración (opcional)
        
    Returns:
        WebLogHandler configurado o None
    """
    try:
        # Importar aquí para evitar dependencias circulares
        from .web_log_handler import WebLogHandler
        
        manager = WebLogConfigManager(config_file)
        config = manager.get_config()
        
        if not config.enabled:
            print("🔒 Web logging está deshabilitado en configuración")
            return None
        
        if not manager.validate_config():
            print("❌ Configuración inválida para web logging")
            return None
        
        # Crear handler
        handler = WebLogHandler(
            api_url=f"{config.api_url.rstrip('/')}/logs",
            api_key=config.api_key,
            buffer_size=config.buffer_size,
            batch_size=config.batch_size,
            flush_interval=config.flush_interval,
            max_retries=config.max_retries,
            timeout=config.timeout,
            fallback_file=config.fallback_file if config.fallback_enabled else None,
            level=getattr(logging, config.level.upper())
        )
        
        print("✅ WebLogHandler configurado exitosamente")
        return handler
        
    except Exception as e:
        print(f"❌ Error configurando WebLogHandler: {e}")
        return None