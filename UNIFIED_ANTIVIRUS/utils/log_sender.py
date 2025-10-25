"""
Log Sender - Cliente para enviar logs al servidor web centralizado
================================================================

Este módulo se encarga de enviar los logs generados por el antivirus
a un servidor web centralizado para monitoreo remoto.
"""

import requests
import json
import os
import time
import threading
import uuid
import socket
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import hashlib
import logging

@dataclass
class LogEntry:
    """Estructura para una entrada de log"""
    pc_id: str
    timestamp: str
    level: str
    logger: str
    message: str
    file: str
    line: int
    function: str
    thread: str
    process_id: int
    
class LogSender:
    """
    Cliente para enviar logs al servidor web centralizado
    """
    
    def __init__(self, server_url_or_config: str, pc_id: Optional[str] = None, 
                 send_interval: int = 30, batch_size: int = 100,
                 log_dir: str = "logs", max_retries: int = 3):
        """
        Inicializa el cliente de envío de logs
        
        Args:
            server_url_or_config: URL del servidor web (ej: http://servidor:5000) o ruta al archivo de configuración JSON
            pc_id: ID único de esta PC (se genera automáticamente si no se proporciona)
            send_interval: Intervalo en segundos para enviar logs
            batch_size: Número máximo de logs por envío
            log_dir: Directorio donde están los logs
            max_retries: Número máximo de reintentos por envío
        """
        # Determinar si es un archivo de configuración o URL directa
        if os.path.isfile(server_url_or_config):
            config = self._load_config(server_url_or_config)
            self.server_url = config.get('server_url', 'http://localhost:8888').rstrip('/')
            self.send_interval = config.get('send_interval', send_interval)
            self.batch_size = config.get('batch_size', batch_size)
            self.max_retries = config.get('retry_attempts', max_retries)
            self.api_endpoint = config.get('api_endpoint', '/api/recibir_logs')
        else:
            self.server_url = server_url_or_config.rstrip('/')
            self.send_interval = send_interval
            self.batch_size = batch_size
            self.max_retries = max_retries
            self.api_endpoint = '/api/recibir_logs'
        
        self.pc_id = pc_id or self._generate_pc_id()
        self.log_dir = Path(log_dir)
        
        # Construir URL completa
        self.full_url = self.server_url + self.api_endpoint
        
        # Control de threads
        self._running = False
        self._sender_thread = None
        self._lock = threading.Lock()
        
        # Buffer para logs pendientes
        self._pending_logs: List[Dict[str, Any]] = []
        self._last_sent_positions = {}
        
        # Configurar logger interno
        self.logger = logging.getLogger(f"log_sender_{self.pc_id}")
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Carga configuración desde archivo JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Error cargando configuración de {config_path}: {e}")
            return {}
    
    def _generate_pc_id(self) -> str:
        """Genera un ID único para esta PC"""
        hostname = socket.gethostname()
        mac = hex(uuid.getnode())[2:]
        return f"{hostname}_{mac}"
    
    def _get_pc_info(self) -> Dict[str, Any]:
        """Obtiene información del PC"""
        import platform
        return {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "ip_address": socket.gethostbyname(socket.gethostname())
        }
    
    def _read_log_files(self) -> List[Dict[str, Any]]:
        """Lee archivos de log y extrae nuevas entradas"""
        new_logs = []
        
        # Archivos de log a monitorear
        log_files = [
            "unified_antivirus.log",
            "security_events.log",
            "test_system_structured.jsonl"
        ]
        
        for log_file in log_files:
            log_path = self.log_dir / log_file
            if not log_path.exists():
                continue
                
            try:
                # Obtener posición de la última lectura
                last_position = self._last_sent_positions.get(log_file, 0)
                
                with open(log_path, 'r', encoding='utf-8') as f:
                    f.seek(last_position)
                    new_content = f.read()
                    new_position = f.tell()
                
                if new_content.strip():
                    # Procesar nuevas líneas
                    lines = new_content.strip().split('\n')
                    for line in lines:
                        if line.strip():
                            log_entry = self._parse_log_line(line, log_file)
                            if log_entry:
                                new_logs.append(log_entry)
                    
                    # Actualizar posición
                    self._last_sent_positions[log_file] = new_position
                    
            except Exception as e:
                self.logger.error(f"Error leyendo {log_file}: {e}")
        
        return new_logs
    
    def _parse_log_line(self, line: str, source_file: str) -> Optional[Dict[str, Any]]:
        """Parsea una línea de log y la convierte a estructura estándar"""
        try:
            # Intentar parsear como JSON (para logs estructurados)
            if line.startswith('{') and line.endswith('}'):
                data = json.loads(line)
                return {
                    "pc_id": self.pc_id,
                    "timestamp": data.get("timestamp", datetime.now().isoformat()),
                    "level": data.get("level", "INFO"),
                    "logger": data.get("logger", "unknown"),
                    "message": data.get("message", ""),
                    "source_file": source_file,
                    "raw_log": line,
                    "parsed": True
                }
            
            # Parseo de logs de texto plano
            # Formato típico: 2025-10-25 10:30:45 - logger_name - INFO - message
            parts = line.split(' - ', 3)
            if len(parts) >= 4:
                timestamp_str, logger_name, level, message = parts
                return {
                    "pc_id": self.pc_id,
                    "timestamp": timestamp_str,
                    "level": level,
                    "logger": logger_name,
                    "message": message,
                    "source_file": source_file,
                    "raw_log": line,
                    "parsed": True
                }
            
            # Si no se puede parsear, enviar como raw
            return {
                "pc_id": self.pc_id,
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "logger": "raw",
                "message": line,
                "source_file": source_file,
                "raw_log": line,
                "parsed": False
            }
            
        except Exception as e:
            self.logger.error(f"Error parseando línea de log: {e}")
            return None
    
    def _send_logs_batch(self, logs: List[Dict[str, Any]]) -> bool:
        """Envía un lote de logs al servidor"""
        if not logs:
            return True
            
        payload = {
            "pc_id": self.pc_id,
            "pc_info": self._get_pc_info(),
            "logs": logs,
            "batch_info": {
                "count": len(logs),
                "timestamp": datetime.now().isoformat(),
                "checksum": hashlib.md5(json.dumps(logs, sort_keys=True).encode()).hexdigest()
            }
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.full_url,
                    json=payload,
                    timeout=30,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "success":
                        self.logger.info(f"Enviados {len(logs)} logs exitosamente")
                        return True
                    else:
                        self.logger.warning(f"Servidor rechazó logs: {result.get('message')}")
                        return False
                else:
                    self.logger.warning(f"Error HTTP {response.status_code}: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error enviando logs (intento {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Backoff exponencial
        
        return False
    
    def _sender_loop(self):
        """Bucle principal del hilo de envío"""
        self.logger.info(f"Iniciado servicio de envío de logs (PC: {self.pc_id})")
        
        while self._running:
            try:
                # Leer nuevos logs
                new_logs = self._read_log_files()
                
                with self._lock:
                    self._pending_logs.extend(new_logs)
                    
                    # Enviar por lotes si hay suficientes logs
                    if len(self._pending_logs) >= self.batch_size:
                        batch = self._pending_logs[:self.batch_size]
                        if self._send_logs_batch(batch):
                            self._pending_logs = self._pending_logs[self.batch_size:]
                        else:
                            # Si falla el envío, mantener logs para reintento
                            self.logger.warning("Fallo envío, logs quedan pendientes")
                
                # Esperar antes del próximo ciclo
                time.sleep(self.send_interval)
                
            except Exception as e:
                self.logger.error(f"Error en bucle de envío: {e}")
                time.sleep(5)
    
    def start(self):
        """Inicia el servicio de envío de logs"""
        if self._running:
            return
            
        self._running = True
        self._sender_thread = threading.Thread(target=self._sender_loop, daemon=True)
        self._sender_thread.start()
        self.logger.info("Servicio de envío de logs iniciado")
    
    def stop(self):
        """Detiene el servicio de envío de logs"""
        if not self._running:
            return
            
        self._running = False
        if self._sender_thread:
            self._sender_thread.join(timeout=10)
        
        # Enviar logs pendientes antes de cerrar
        with self._lock:
            if self._pending_logs:
                self.logger.info(f"Enviando {len(self._pending_logs)} logs pendientes...")
                self._send_logs_batch(self._pending_logs)
                self._pending_logs.clear()
        
        self.logger.info("Servicio de envío de logs detenido")
    
    def send_manual_log(self, level: str, message: str, logger_name: str = "manual"):
        """Envía un log manual inmediatamente"""
        log_entry = {
            "pc_id": self.pc_id,
            "timestamp": datetime.now().isoformat(),
            "level": level.upper(),
            "logger": logger_name,
            "message": message,
            "source_file": "manual",
            "raw_log": f"[MANUAL] {level}: {message}",
            "parsed": True
        }
        
        return self._send_logs_batch([log_entry])
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado del servicio"""
        with self._lock:
            return {
                "running": self._running,
                "pc_id": self.pc_id,
                "server_url": self.server_url,
                "pending_logs": len(self._pending_logs),
                "last_positions": self._last_sent_positions.copy(),
                "send_interval": self.send_interval,
                "batch_size": self.batch_size
            }

# Instancia global del sender (singleton)
_global_log_sender: Optional[LogSender] = None

def init_log_sender(server_url: str, **kwargs) -> LogSender:
    """Inicializa el servicio global de envío de logs"""
    global _global_log_sender
    _global_log_sender = LogSender(server_url, **kwargs)
    return _global_log_sender

def get_log_sender() -> Optional[LogSender]:
    """Obtiene la instancia global del log sender"""
    return _global_log_sender

def start_log_sender():
    """Inicia el servicio global de envío de logs"""
    if _global_log_sender:
        _global_log_sender.start()

def stop_log_sender():
    """Detiene el servicio global de envío de logs"""
    if _global_log_sender:
        _global_log_sender.stop()


# Ejemplo de uso
if __name__ == "__main__":
    # Configuración de ejemplo
    sender = LogSender(
        server_url="http://localhost:8000",
        send_interval=10,  # Enviar cada 10 segundos para pruebas
        batch_size=5
    )
    
    print(f"PC ID: {sender.pc_id}")
    print(f"Estado: {sender.get_status()}")
    
    # Enviar un log de prueba
    sender.send_manual_log("INFO", "Log de prueba desde cliente")
    
    # Iniciar servicio automático
    sender.start()
    
    try:
        print("Servicio de envío iniciado. Presiona Ctrl+C para detener...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo servicio...")
        sender.stop()