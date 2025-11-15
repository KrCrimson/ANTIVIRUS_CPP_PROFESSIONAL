"""
Web Log Handler - HTTP Handler para envío de logs al backend web
===============================================================

Handler personalizado de logging que envía logs al backend FastAPI
mediante HTTP requests con buffer, reconexión automática y fallback.
"""

import logging
import requests
import json
import threading
import time
import queue
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path
import os


class WebLogHandler(logging.Handler):
    """
    Handler de logging que envía logs al backend web via HTTP POST
    
    Características:
    - Buffer local para logs offline
    - Reconexión automática 
    - Fallback a archivo si falla
    - Rate limiting interno
    - Batch processing para performance
    """
    
    def __init__(self, 
                 api_url: str,
                 api_key: str,
                 buffer_size: int = 1000,
                 batch_size: int = 10,
                 flush_interval: float = 5.0,
                 max_retries: int = 3,
                 timeout: float = 10.0,
                 fallback_file: Optional[str] = None,
                 level: int = logging.INFO):
        """
        Inicializa el WebLogHandler
        
        Args:
            api_url: URL del endpoint de logs (ej: http://localhost:8000/api/logs)
            api_key: API key para autenticación
            buffer_size: Tamaño máximo del buffer local
            batch_size: Número de logs a enviar por batch
            flush_interval: Intervalo de envío en segundos
            max_retries: Máximo número de reintentos
            timeout: Timeout para requests HTTP
            fallback_file: Archivo de fallback si falla el envío
            level: Nivel mínimo de logging
        """
        super().__init__(level)
        
        # Configuración
        self.api_url = api_url.rstrip('/') + ('/logs' if not api_url.endswith('/logs') else '')
        self.api_key = api_key
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.max_retries = max_retries
        self.timeout = timeout
        
        # Buffer y threading
        self.buffer = queue.Queue(maxsize=buffer_size)
        self.is_running = True
        self.last_flush = datetime.now()
        
        # Fallback file handler
        self.fallback_handler = None
        if fallback_file:
            self._setup_fallback_handler(fallback_file)
        
        # Estadísticas
        self.stats = {
            'logs_sent': 0,
            'logs_failed': 0,
            'logs_buffered': 0,
            'last_success': None,
            'last_error': None,
            'is_connected': False
        }
        
        # Lock para thread safety
        self._lock = threading.Lock()
        
        # Iniciar worker thread
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        
        # Headers HTTP
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key,
            'User-Agent': 'AntivirusLogger/1.0'
        }
        
        # Test inicial de conectividad
        self._test_connection()
    
    def _setup_fallback_handler(self, fallback_file: str):
        """Configura handler de fallback a archivo"""
        try:
            fallback_path = Path(fallback_file)
            fallback_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.fallback_handler = logging.FileHandler(
                fallback_file, 
                encoding='utf-8',
                mode='a'
            )
            self.fallback_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
            )
        except Exception as e:
            print(f"⚠️ Error configurando fallback handler: {e}")
    
    def _test_connection(self):
        """Test inicial de conectividad con el backend"""
        try:
            # Probar endpoint de health
            health_url = self.api_url.replace('/logs', '/health')
            response = requests.get(health_url, timeout=5)
            
            if response.status_code == 200:
                self.stats['is_connected'] = True
                self.stats['last_success'] = datetime.now()
                print(f"✅ WebLogHandler conectado a {self.api_url}")
            else:
                raise requests.RequestException(f"Health check failed: {response.status_code}")
                
        except Exception as e:
            self.stats['is_connected'] = False
            self.stats['last_error'] = str(e)
            print(f"⚠️ WebLogHandler no pudo conectar: {e}")
    
    def emit(self, record: logging.LogRecord):
        """
        Método principal del handler - procesa cada log record
        
        Args:
            record: Log record de Python logging
        """
        if not self.is_running:
            return
        
        try:
            # Convertir LogRecord a formato JSON para API
            log_data = self._format_log_record(record)
            
            # Agregar al buffer (non-blocking)
            try:
                self.buffer.put_nowait(log_data)
                with self._lock:
                    self.stats['logs_buffered'] += 1
            except queue.Full:
                # Buffer lleno - usar fallback
                if self.fallback_handler:
                    self.fallback_handler.emit(record)
                with self._lock:
                    self.stats['logs_failed'] += 1
                    
        except Exception as e:
            # Error formateando - usar fallback
            if self.fallback_handler:
                self.fallback_handler.emit(record)
            print(f"❌ Error en WebLogHandler.emit: {e}")
    
    def _format_log_record(self, record: logging.LogRecord) -> Dict[str, Any]:
        """
        Convierte LogRecord a formato esperado por el API
        
        Args:
            record: LogRecord de Python logging
            
        Returns:
            Dict con formato del API
        """
        # Datos base
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'component': record.name,
            'details': {
                'module': record.module,
                'function': record.funcName,
                'line_number': record.lineno,
                'thread_id': record.thread,
                'process_id': record.process
            }
        }
        
        # Agregar datos extra si existen
        if hasattr(record, 'extra_data'):
            log_data['details'].update(record.extra_data)
        
        # Agregar información de excepción si existe
        if record.exc_info:
            log_data['details']['exception'] = self.formatException(record.exc_info)
        
        # Agregar stack info si está disponible
        if hasattr(record, 'stack_info') and record.stack_info:
            log_data['details']['stack_info'] = record.stack_info
        
        return log_data
    
    def _worker_loop(self):
        """
        Loop principal del worker thread - envía logs en batches
        """
        batch = []
        
        while self.is_running:
            try:
                # Recoger logs del buffer con timeout
                try:
                    log_data = self.buffer.get(timeout=1.0)
                    batch.append(log_data)
                except queue.Empty:
                    pass
                
                # Enviar batch si:
                # 1. Alcanzamos el tamaño de batch
                # 2. Ha pasado el flush_interval
                # 3. El sistema se está cerrando
                should_flush = (
                    len(batch) >= self.batch_size or
                    (batch and (datetime.now() - self.last_flush).total_seconds() >= self.flush_interval) or
                    not self.is_running
                )
                
                if should_flush and batch:
                    self._send_batch(batch)
                    batch = []
                    self.last_flush = datetime.now()
                    
            except Exception as e:
                print(f"❌ Error en worker loop: {e}")
                time.sleep(1)
    
    def _send_batch(self, batch: List[Dict[str, Any]]):
        """
        Envía un batch de logs al backend
        
        Args:
            batch: Lista de logs a enviar
        """
        if not batch:
            return
        
        for attempt in range(self.max_retries + 1):
            try:
                # Enviar cada log individualmente (el API espera logs individuales)
                success_count = 0
                
                for log_data in batch:
                    response = requests.post(
                        self.api_url,
                        json=log_data,
                        headers=self.headers,
                        timeout=self.timeout
                    )
                    
                    if response.status_code in [200, 201]:
                        success_count += 1
                    else:
                        raise requests.RequestException(
                            f"HTTP {response.status_code}: {response.text}"
                        )
                
                # Actualizar estadísticas de éxito
                with self._lock:
                    self.stats['logs_sent'] += success_count
                    self.stats['logs_buffered'] -= len(batch)
                    self.stats['last_success'] = datetime.now()
                    self.stats['is_connected'] = True
                
                break  # Éxito - salir del loop de reintentos
                
            except Exception as e:
                with self._lock:
                    self.stats['last_error'] = str(e)
                    self.stats['is_connected'] = False
                
                if attempt < self.max_retries:
                    # Backoff exponencial
                    wait_time = (2 ** attempt) * 1.0
                    print(f"⚠️ Error enviando logs (intento {attempt + 1}/{self.max_retries + 1}). "
                          f"Reintentando en {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    # Falló todos los intentos - usar fallback
                    print(f"❌ Error enviando logs después de {self.max_retries + 1} intentos: {e}")
                    
                    if self.fallback_handler:
                        for log_data in batch:
                            # Crear LogRecord fake para fallback
                            fake_record = logging.LogRecord(
                                name=log_data.get('component', 'unknown'),
                                level=getattr(logging, log_data.get('level', 'INFO')),
                                pathname='',
                                lineno=0,
                                msg=log_data.get('message', ''),
                                args=(),
                                exc_info=None
                            )
                            self.fallback_handler.emit(fake_record)
                    
                    with self._lock:
                        self.stats['logs_failed'] += len(batch)
                        self.stats['logs_buffered'] -= len(batch)
    
    def flush(self):
        """Fuerza el envío de todos los logs pendientes"""
        # Enviar logs restantes en el buffer
        batch = []
        try:
            while True:
                log_data = self.buffer.get_nowait()
                batch.append(log_data)
        except queue.Empty:
            pass
        
        if batch:
            self._send_batch(batch)
    
    def close(self):
        """Cierra el handler limpiamente"""
        self.is_running = False
        
        # Flush logs pendientes
        self.flush()
        
        # Esperar que termine el worker thread
        if self.worker_thread.is_alive():
            self.worker_thread.join(timeout=5)
        
        # Cerrar fallback handler
        if self.fallback_handler:
            self.fallback_handler.close()
        
        super().close()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del handler
        
        Returns:
            Dict con estadísticas de funcionamiento
        """
        with self._lock:
            return {
                **self.stats,
                'buffer_size': self.buffer.qsize(),
                'max_buffer_size': self.buffer_size,
                'api_url': self.api_url,
                'batch_size': self.batch_size,
                'flush_interval': self.flush_interval
            }
    
    def test_connection(self) -> bool:
        """
        Test manual de conectividad
        
        Returns:
            True si la conexión es exitosa
        """
        try:
            # Enviar log de test
            test_log = {
                'timestamp': datetime.now().isoformat(),
                'level': 'INFO',
                'message': 'WebLogHandler connection test',
                'component': 'web_handler_test',
                'details': {
                    'test': True,
                    'handler_id': id(self)
                }
            }
            
            response = requests.post(
                self.api_url,
                json=test_log,
                headers=self.headers,
                timeout=self.timeout
            )
            
            success = response.status_code in [200, 201]
            
            with self._lock:
                if success:
                    self.stats['is_connected'] = True
                    self.stats['last_success'] = datetime.now()
                else:
                    self.stats['is_connected'] = False
                    self.stats['last_error'] = f"HTTP {response.status_code}"
            
            return success
            
        except Exception as e:
            with self._lock:
                self.stats['is_connected'] = False
                self.stats['last_error'] = str(e)
            return False


# =================== CONVENIENCE FUNCTIONS ===================
def create_web_log_handler(config: Dict[str, Any]) -> Optional[WebLogHandler]:
    """
    Crea un WebLogHandler desde configuración
    
    Args:
        config: Diccionario de configuración
        
    Returns:
        WebLogHandler configurado o None si falla
    """
    try:
        return WebLogHandler(
            api_url=config['api_url'],
            api_key=config['api_key'],
            buffer_size=config.get('buffer_size', 1000),
            batch_size=config.get('batch_size', 10),
            flush_interval=config.get('flush_interval', 5.0),
            max_retries=config.get('max_retries', 3),
            timeout=config.get('timeout', 10.0),
            fallback_file=config.get('fallback_file'),
            level=getattr(logging, config.get('level', 'INFO').upper())
        )
    except Exception as e:
        print(f"❌ Error creando WebLogHandler: {e}")
        return None