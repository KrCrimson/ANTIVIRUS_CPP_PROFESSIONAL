"""
Web Log Handler - Plugin para enviar logs al backend web
========================================================

Plugin que intercepta los logs del sistema y los envía al backend web
para almacenamiento persistente y visualización en dashboard.
"""

import json
import asyncio
import aiohttp
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from collections import deque
import uuid
import socket
import platform
import threading
import logging

from core.base_plugin import BasePlugin
from core.event_bus import event_bus
from utils.logger import get_logger

logger = get_logger(__name__)

class WebLogHandlerPlugin(BasePlugin):
    """Plugin para envío de logs al backend web"""
    
    def __init__(self, plugin_name: str, plugin_path: str):
        super().__init__(plugin_name, plugin_path)
        self.enabled = self.config.get("enabled", True)
        
        # Configuración del backend
        self.api_url = self.config.get("api_url", "http://localhost:8000/api")
        self.api_key = self.config.get("api_key", "antivirus-system-key-2024")
        self.bypass_token = self.config.get("bypass_token")
        self.batch_size = self.config.get("batch_size", 10)
        self.flush_interval = self.config.get("flush_interval", 5.0)
        self.timeout = self.config.get("timeout", 30.0)
        self.max_retries = self.config.get("max_retries", 3)
        self.buffer_size = self.config.get("buffer_size", 1000)
        
        # Buffer de logs
        self.log_buffer = deque(maxlen=self.buffer_size)
        self.buffer_lock = threading.RLock()
        
        # Estado del sender
        self.sender_task = None
        self.sender_running = False
        self.session = None
        
        # ID único de la instancia
        self.instance_id = self._generate_instance_id()
        
        # Estadísticas
        self.stats = {
            "logs_sent": 0,
            "logs_failed": 0,
            "last_send": None,
            "connection_errors": 0
        }
        
        logger.info(f"[WEB_LOG_HANDLER] Inicializado - Instance ID: {self.instance_id}")
        
    async def _initialize_async(self):
        """Inicialización asíncrona del plugin"""
        try:
            # Crear sesión HTTP con headers apropiados (ahora en el event loop)
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                headers=self.session_headers
            )
            logger.info("✅ Sesión HTTP creada exitosamente")
            
            # Verificar conectividad con health check
            health_ok = await self._health_check()
            if health_ok:
                logger.info("✅ WebLogHandler conectado exitosamente al backend")
                # Registrar la instancia en el backend
                await self._register_instance()
            else:
                logger.warning("❌ WebLogHandler no pudo conectar: Health check failed")
        except Exception as e:
            logger.error(f"[WEB_LOG_HANDLER] Error en inicialización async: {e}")
        
    async def _health_check(self) -> bool:
        """Verifica conectividad con el backend"""
        try:
            health_url = self._build_url("/health")
            async with self.session.get(health_url) as response:
                if response.status == 200:
                    return True
                else:
                    logger.warning(f"Health check failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return False
    
    def _build_url(self, endpoint: str) -> str:
        """Construye URL con bypass token si está disponible"""
        url = f"{self.api_url}{endpoint}"
        if self.bypass_token:
            separator = "&" if "?" in url else "?"
            url += f"{separator}x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass={self.bypass_token}"
        return url
    
    def _generate_instance_id(self) -> str:
        """Genera ID único para esta instancia del antivirus"""
        hostname = socket.gethostname()
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d")
        unique_id = str(uuid.uuid4())[:8]
        return f"{hostname}-{unique_id}-{timestamp}"
    
    def get_plugin_info(self) -> Dict[str, Any]:
        """Retorna información del plugin"""
        return {
            "name": "web_log_handler",
            "version": "1.2.0",
            "category": "handlers", 
            "description": "Handler para envío de logs al backend web",
            "enabled": self.enabled,
            "api_url": self.api_url,
            "instance_id": self.instance_id
        }
    
    def initialize(self) -> bool:
        """Inicializa el plugin"""
        try:
            if not self.enabled:
                logger.info("[WEB_LOG_HANDLER] Plugin deshabilitado en configuración")
                return True
            
            # Preparar headers para la sesión HTTP (se creará en el thread asyncio)
            self.session_headers = {
                "X-API-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            # Nota: No ejecutamos _initialize_async aquí porque no hay event loop
            # Se ejecutará automáticamente cuando se inicie el plugin en start()
            
            logger.info("✅ WebLogHandler configurado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"[WEB_LOG_HANDLER] Error inicializando: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def start(self) -> bool:
        """Inicia el plugin"""
        try:
            if not self.enabled:
                return True
            
            # Suscribirse a eventos de logs PRIMERO
            event_bus.subscribe("log_generated", self._on_log_generated, "web_log_handler")
            event_bus.subscribe("threat_detected", self._on_threat_detected, "web_log_handler") 
            event_bus.subscribe("security_alert", self._on_security_alert, "web_log_handler")
            logger.info("[WEB_LOG_HANDLER] Suscripciones a eventos completadas")
            
            # Iniciar el task de envío de logs en background con thread separado
            self.sender_running = True
            
            import threading
            def run_async_loop():
                try:
                    # Crear un nuevo event loop para este thread
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    
                    # Ejecutar inicialización asyncronizada y luego el sender
                    new_loop.run_until_complete(self._initialize_async())
                    self.sender_task = new_loop.create_task(self._log_sender_loop())
                    new_loop.run_forever()
                    
                except Exception as e:
                    logger.error(f"[WEB_LOG_HANDLER] Error en thread asyncio: {e}")
            
            self.async_thread = threading.Thread(target=run_async_loop, daemon=True)
            self.async_thread.start()
            
            logger.info("[WEB_LOG_HANDLER] Plugin iniciado - Sender activado en thread separado")
            return True
            
        except Exception as e:
            logger.error(f"[WEB_LOG_HANDLER] Error iniciando: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def stop(self) -> None:
        """Detiene el plugin"""
        try:
            logger.info("[WEB_LOG_HANDLER] Deteniendo plugin...")
            
            # Detener el sender
            self.sender_running = False
            if self.sender_task:
                self.sender_task.cancel()
            
            # Enviar logs pendientes
            if self.log_buffer:
                asyncio.create_task(self._flush_remaining_logs())
            
            # Cerrar sesión HTTP
            if self.session:
                asyncio.create_task(self.session.close())
            
            # Desuscribirse de eventos
            event_bus.unsubscribe("log_generated", self._on_log_generated)
            event_bus.unsubscribe("threat_detected", self._on_threat_detected)
            event_bus.unsubscribe("security_alert", self._on_security_alert)
            
            logger.info("[WEB_LOG_HANDLER] Plugin detenido")
            
        except Exception as e:
            logger.error(f"[WEB_LOG_HANDLER] Error deteniendo: {e}")
    
    def cleanup(self) -> None:
        """Limpia recursos del plugin"""
        self.stop()
    
    async def _register_instance(self):
        """Registra esta instancia en el backend"""
        try:
            instance_data = {
                "id": self.instance_id,
                "hostname": socket.gethostname(),
                "os_info": f"{platform.system()} {platform.release()}",
                "antivirus_version": "1.2.0",
                "status": "active",
                "registered_at": datetime.now(timezone.utc).isoformat()
            }
            
            register_url = self._build_url("/instances")
            async with self.session.post(
                register_url,
                json=instance_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"[WEB_LOG_HANDLER] Instancia registrada: {result}")
                else:
                    logger.warning(f"[WEB_LOG_HANDLER] Error registrando instancia: {response.status}")
                    
        except Exception as e:
            logger.error(f"[WEB_LOG_HANDLER] Error registrando instancia: {e}")
            self.stats["connection_errors"] += 1
    
    def _on_log_generated(self, event):
        """Maneja eventos de logs generados"""
        try:
            # El evento es un objeto Event, los datos están en event.data
            event_data = event.data
            
            # Convertir el log a formato para envío
            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": event_data.get("level", "INFO"),
                "component": event_data.get("logger_name", "Unknown"),
                "message": event_data.get("message", ""),
                "instance_id": self.instance_id,
                "details": {
                    "function": event_data.get("function"),
                    "line": event_data.get("line"),
                    "module": event_data.get("module"),
                    "extra": event_data.get("extra", {})
                }
            }
            
            # Agregar al buffer
            with self.buffer_lock:
                self.log_buffer.append(log_entry)
            
        except Exception as e:
            logger.error(f"[WEB_LOG_HANDLER] Error procesando log: {e}")
    
    def _on_threat_detected(self, event):
        """Maneja eventos de amenazas detectadas"""
        try:
            # El evento es un objeto Event, los datos están en event.data
            event_data = event.data
            
            # Crear log especial para amenaza detectada
            threat_log = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": "WARNING",
                "component": "ThreatDetector",
                "message": f"[DETECTION] {event_data.get('description', 'Amenaza detectada')}",
                "instance_id": self.instance_id,
                "details": {
                    "threat_type": event_data.get("threat_type"),
                    "severity": event_data.get("severity"),
                    "source": event_data.get("source"),
                    "metadata": event_data.get("metadata", {})
                }
            }
            
            # Agregar al buffer con prioridad alta
            with self.buffer_lock:
                self.log_buffer.appendleft(threat_log)  # Al inicio para envío prioritario
            
        except Exception as e:
            logger.error(f"[WEB_LOG_HANDLER] Error procesando amenaza: {e}")
    
    def _on_security_alert(self, event):
        """Maneja eventos de alertas de seguridad"""
        try:
            # El evento es un objeto Event, los datos están en event.data
            event_data = event.data
            
            # Crear log especial para alerta de seguridad
            security_log = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": "WARNING",
                "component": f"SecurityAlert-{event_data.get('plugin', 'Unknown')}",
                "message": f"[ALERT] {event_data.get('description', 'Alerta de seguridad')}",
                "instance_id": self.instance_id,
                "details": {
                    "alert_type": event_data.get("type"),
                    "severity": event_data.get("severity"),
                    "process_info": event_data.get("process_info", {}),
                    "plugin": event_data.get("plugin"),
                    "timestamp": event_data.get("timestamp")
                }
            }
            
            # Agregar al buffer con prioridad alta
            with self.buffer_lock:
                self.log_buffer.appendleft(security_log)  # Al inicio para envío prioritario
                
            logger.debug(f"[WEB_LOG_HANDLER] Alerta de seguridad agregada al buffer: {event_data.get('type')}")
            
        except Exception as e:
            logger.error(f"[WEB_LOG_HANDLER] Error procesando alerta de seguridad: {e}")
    
    async def _log_sender_loop(self):
        """Loop principal para envío de logs"""
        logger.info("[WEB_LOG_HANDLER] Iniciando loop de envío de logs")
        
        while self.sender_running:
            try:
                await asyncio.sleep(self.flush_interval)
                
                # Obtener batch de logs para enviar
                logs_to_send = []
                with self.buffer_lock:
                    batch_size = min(self.batch_size, len(self.log_buffer))
                    for _ in range(batch_size):
                        if self.log_buffer:
                            logs_to_send.append(self.log_buffer.popleft())
                
                # Enviar logs si hay alguno
                if logs_to_send:
                    await self._send_logs_batch(logs_to_send)
                
            except asyncio.CancelledError:
                logger.info("[WEB_LOG_HANDLER] Sender loop cancelado")
                break
            except Exception as e:
                logger.error(f"[WEB_LOG_HANDLER] Error en sender loop: {e}")
                await asyncio.sleep(5)  # Wait before retry
    
    async def _send_logs_batch(self, logs: List[Dict[str, Any]]):
        """Envía un batch de logs al backend"""
        for attempt in range(self.max_retries):
            try:
                # Enviar cada log individualmente
                logs_url = self._build_url("/logs")
                for log_entry in logs:
                    async with self.session.post(
                        logs_url,
                        json=log_entry
                    ) as response:
                        if response.status == 200:
                            self.stats["logs_sent"] += 1
                        else:
                            logger.warning(f"[WEB_LOG_HANDLER] Error enviando log: {response.status}")
                            self.stats["logs_failed"] += 1
                
                self.stats["last_send"] = datetime.now(timezone.utc).isoformat()
                logger.debug(f"[WEB_LOG_HANDLER] Enviados {len(logs)} logs exitosamente")
                return
                
            except Exception as e:
                logger.error(f"[WEB_LOG_HANDLER] Error enviando batch (intento {attempt + 1}): {e}")
                self.stats["connection_errors"] += 1
                
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    # Devolver logs al buffer si falló completamente
                    with self.buffer_lock:
                        for log in reversed(logs):
                            self.log_buffer.appendleft(log)
                    self.stats["logs_failed"] += len(logs)
    
    async def _flush_remaining_logs(self):
        """Envía logs restantes al detener el plugin"""
        try:
            remaining_logs = []
            with self.buffer_lock:
                while self.log_buffer:
                    remaining_logs.append(self.log_buffer.popleft())
            
            if remaining_logs:
                logger.info(f"[WEB_LOG_HANDLER] Enviando {len(remaining_logs)} logs restantes...")
                await self._send_logs_batch(remaining_logs)
                
        except Exception as e:
            logger.error(f"[WEB_LOG_HANDLER] Error enviando logs restantes: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del plugin"""
        return {
            "plugin_name": self.plugin_name,
            "enabled": self.enabled,
            "sender_running": self.sender_running,
            "buffer_size": len(self.log_buffer),
            "instance_id": self.instance_id,
            "api_url": self.api_url,
            "stats": self.stats.copy()
        }

# Función de factory requerida por el sistema de plugins
def create_plugin(config: Dict[str, Any]) -> WebLogHandlerPlugin:
    """Crea una instancia del plugin"""
    return WebLogHandlerPlugin(config)