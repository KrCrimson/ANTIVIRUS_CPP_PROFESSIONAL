"""
Unified Antivirus - Web Log Sender
=================================

Cliente para enviar logs del antivirus al backend centralizado en Vercel.
Maneja el envío asíncrono de logs, retry logic y buffering local.
"""

import asyncio
import aiohttp
import json
import time
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import platform
import queue
import threading
from dataclasses import dataclass, asdict
import logging

# Configuración
DEFAULT_API_ENDPOINT = "https://unified-antivirus-duzz48bmm-sebastians-projects-487d2baa.vercel.app/api/logs"
DEFAULT_API_KEY = "antivirus-key-2024-prod-12345"
BATCH_SIZE = 50
SEND_INTERVAL = 30  # segundos
MAX_RETRIES = 3
BUFFER_MAX_SIZE = 1000


@dataclass
class LogEntry:
    """Estructura de un log entry"""
    timestamp: str
    level: str
    logger: str
    message: str
    module: Optional[str] = None
    function: Optional[str] = None
    line: Optional[int] = None
    component: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class WebLogSender:
    """Cliente para envío de logs al backend centralizado"""
    
    def __init__(
        self,
        api_endpoint: str = DEFAULT_API_ENDPOINT,
        api_key: str = DEFAULT_API_KEY,
        client_id: Optional[str] = None,
        antivirus_version: str = "1.0.0"
    ):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.client_id = client_id or self._generate_client_id()
        self.antivirus_version = antivirus_version
        
        # Información del sistema
        self.hostname = platform.node()
        self.os_info = f"{platform.system()} {platform.release()}"
        
        # Buffer interno
        self.log_buffer: queue.Queue = queue.Queue(maxsize=BUFFER_MAX_SIZE)
        self.stats = {
            "total_sent": 0,
            "total_failed": 0,
            "last_send": None,
            "connection_errors": 0
        }
        
        # Control de hilos
        self.running = False
        self.sender_thread = None
        self.session = None
        
        # Logger interno
        self.logger = logging.getLogger(f"web_log_sender_{self.client_id}")
        
    def _generate_client_id(self) -> str:
        """Genera un ID único para el cliente"""
        hostname = platform.node()
        return f"{hostname}_{uuid.uuid4().hex[:8]}"
    
    async def start(self):
        """Inicia el cliente de envío de logs"""
        if self.running:
            return
            
        self.running = True
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
                "User-Agent": f"UnifiedAntivirus/{self.antivirus_version}"
            }
        )
        
        # Iniciar hilo de envío
        self.sender_thread = threading.Thread(target=self._sender_loop, daemon=True)
        self.sender_thread.start()
        
        self.logger.info(f"WebLogSender iniciado - ClientID: {self.client_id}")
        
    async def stop(self):
        """Detiene el cliente y envía logs pendientes"""
        if not self.running:
            return
            
        self.running = False
        
        # Enviar logs pendientes
        await self._send_buffered_logs()
        
        # Cerrar sesión HTTP
        if self.session:
            await self.session.close()
            
        # Esperar a que termine el hilo
        if self.sender_thread and self.sender_thread.is_alive():
            self.sender_thread.join(timeout=5)
            
        self.logger.info("WebLogSender detenido")
    
    def add_log(
        self,
        level: str,
        logger: str,
        message: str,
        module: Optional[str] = None,
        function: Optional[str] = None,
        line: Optional[int] = None,
        component: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Añade un log al buffer para envío"""
        if not self.running:
            return False
            
        log_entry = LogEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            level=level.upper(),
            logger=logger,
            message=message,
            module=module,
            function=function,
            line=line,
            component=component,
            metadata=metadata
        )
        
        try:
            self.log_buffer.put_nowait(log_entry)
            return True
        except queue.Full:
            self.logger.warning("Buffer de logs lleno, descartando log más antiguo")
            try:
                self.log_buffer.get_nowait()  # Remover el más antiguo
                self.log_buffer.put_nowait(log_entry)
                return True
            except queue.Empty:
                return False
    
    def _sender_loop(self):
        """Loop principal de envío de logs"""
        while self.running:
            try:
                # Esperar intervalo de envío
                for _ in range(SEND_INTERVAL):
                    if not self.running:
                        break
                    time.sleep(1)
                
                if not self.running:
                    break
                    
                # Enviar logs en batch
                asyncio.run(self._send_buffered_logs())
                
            except Exception as e:
                self.logger.error(f"Error in sender loop: {e}")
                time.sleep(5)  # Esperar antes de reintentar
    
    async def _send_buffered_logs(self):
        """Envía logs del buffer al servidor"""
        if self.log_buffer.empty():
            return
            
        # Recopilar logs del buffer
        logs_to_send = []
        while not self.log_buffer.empty() and len(logs_to_send) < BATCH_SIZE:
            try:
                log_entry = self.log_buffer.get_nowait()
                logs_to_send.append(asdict(log_entry))
            except queue.Empty:
                break
        
        if not logs_to_send:
            return
            
        # Preparar payload
        payload = {
            "clientId": self.client_id,
            "hostname": self.hostname,
            "version": self.antivirus_version,
            "os": self.os_info,
            "logs": logs_to_send
        }
        
        # Intentar envío con reintentos
        success = False
        for attempt in range(MAX_RETRIES):
            try:
                async with self.session.post(self.api_endpoint, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.stats["total_sent"] += len(logs_to_send)
                        self.stats["last_send"] = datetime.now()
                        self.logger.info(f"Enviados {len(logs_to_send)} logs exitosamente")
                        success = True
                        break
                    else:
                        error_text = await response.text()
                        self.logger.warning(f"Error HTTP {response.status}: {error_text}")
                        
            except aiohttp.ClientError as e:
                self.stats["connection_errors"] += 1
                self.logger.warning(f"Error de conexión (intento {attempt + 1}): {e}")
                
            except Exception as e:
                self.logger.error(f"Error inesperado (intento {attempt + 1}): {e}")
            
            # Esperar antes del siguiente intento
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(2 ** attempt)  # Backoff exponencial
        
        if not success:
            # Devolver logs al buffer si falló el envío
            for log_data in reversed(logs_to_send):
                log_entry = LogEntry(**log_data)
                try:
                    self.log_buffer.put_nowait(log_entry)
                except queue.Full:
                    break  # Si el buffer está lleno, perder logs antiguos
                    
            self.stats["total_failed"] += len(logs_to_send)
            self.logger.error(f"Falló el envío de {len(logs_to_send)} logs después de {MAX_RETRIES} intentos")
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del cliente"""
        return {
            **self.stats,
            "client_id": self.client_id,
            "hostname": self.hostname,
            "buffer_size": self.log_buffer.qsize(),
            "running": self.running,
            "last_send_ago": (
                (datetime.now() - self.stats["last_send"]).total_seconds()
                if self.stats["last_send"] else None
            )
        }


# Instancia global del cliente
_global_web_sender: Optional[WebLogSender] = None


async def initialize_web_log_sender(
    api_endpoint: str = DEFAULT_API_ENDPOINT,
    api_key: str = DEFAULT_API_KEY,
    client_id: Optional[str] = None,
    antivirus_version: str = "1.0.0"
) -> WebLogSender:
    """Inicializa el cliente global de envío de logs"""
    global _global_web_sender
    
    if _global_web_sender:
        await _global_web_sender.stop()
    
    _global_web_sender = WebLogSender(
        api_endpoint=api_endpoint,
        api_key=api_key,
        client_id=client_id,
        antivirus_version=antivirus_version
    )
    
    await _global_web_sender.start()
    return _global_web_sender


def send_web_log(
    level: str,
    logger: str,
    message: str,
    module: Optional[str] = None,
    function: Optional[str] = None,
    line: Optional[int] = None,
    component: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """Función helper para enviar un log usando el cliente global"""
    if not _global_web_sender:
        return False
        
    return _global_web_sender.add_log(
        level=level,
        logger=logger,
        message=message,
        module=module,
        function=function,
        line=line,
        component=component,
        metadata=metadata
    )


async def shutdown_web_log_sender():
    """Cierra el cliente global de envío de logs"""
    global _global_web_sender
    if _global_web_sender:
        await _global_web_sender.stop()
        _global_web_sender = None


def get_web_sender_stats() -> Optional[Dict[str, Any]]:
    """Obtiene estadísticas del cliente global"""
    if not _global_web_sender:
        return None
    return _global_web_sender.get_stats()


# Ejemplo de uso
if __name__ == "__main__":
    async def main():
        # Inicializar cliente
        sender = await initialize_web_log_sender()
        
        # Enviar algunos logs de prueba
        send_web_log("INFO", "test_logger", "Test message 1", component="test_component")
        send_web_log("WARNING", "test_logger", "Test warning", component="test_component")
        send_web_log("ERROR", "test_logger", "Test error", component="test_component", 
                    metadata={"error_code": 500, "details": "Test error details"})
        
        # Esperar un momento para que se envíen
        await asyncio.sleep(35)
        
        # Mostrar estadísticas
        stats = get_web_sender_stats()
        print("Estadísticas del web sender:", json.dumps(stats, indent=2, default=str))
        
        # Cerrar
        await shutdown_web_log_sender()
    
    asyncio.run(main())