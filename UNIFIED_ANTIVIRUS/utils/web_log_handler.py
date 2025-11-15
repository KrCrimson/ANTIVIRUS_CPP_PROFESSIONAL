"""
WebLogHandler - Handler personalizado para enviar logs automáticamente al backend
"""

import logging
import json
from datetime import datetime
import threading
import time
from typing import Optional

class WebLogHandler(logging.Handler):
    """Handler que envía logs automáticamente al backend web"""
    
    def __init__(self, web_sender):
        super().__init__()
        self.web_sender = web_sender
        self.buffer = []
        self.buffer_lock = threading.Lock()
        self.last_flush = time.time()
        self.flush_interval = 10  # Enviar cada 10 segundos
        
        # Iniciar thread de envío automático
        self.sender_thread = threading.Thread(target=self._auto_sender, daemon=True)
        self.sender_thread.start()
    
    def emit(self, record):
        """Capturar y almacenar el log para envío"""
        try:
            # Formatear el log
            log_entry = {
                'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                'level': record.levelname,
                'logger': record.name,
                'message': self.format(record),
                'module': getattr(record, 'module', None),
                'function': record.funcName,
                'line': record.lineno,
                'component': self._extract_component(record.name),
                'metadata': {
                    'thread': record.thread,
                    'process': record.process,
                    'filename': record.filename
                }
            }
            
            # Agregar al buffer
            with self.buffer_lock:
                self.buffer.append(log_entry)
                
                # Si el buffer está lleno, forzar envío
                if len(self.buffer) >= 50:
                    self._flush_buffer()
                    
        except Exception as e:
            # No usar logging aquí para evitar recursión
            print(f"Error en WebLogHandler: {e}")
    
    def _extract_component(self, logger_name):
        """Extraer componente del nombre del logger"""
        if 'behavior_detector' in logger_name:
            return 'behavior_detector'
        elif 'ml_detector' in logger_name:
            return 'ml_detector'
        elif 'network_detector' in logger_name:
            return 'network_detector'
        elif 'file_monitor' in logger_name:
            return 'file_monitor'
        elif 'process_monitor' in logger_name:
            return 'process_monitor'
        elif 'alert_manager' in logger_name:
            return 'alert_manager'
        elif 'quarantine' in logger_name:
            return 'quarantine_handler'
        elif 'launcher' in logger_name:
            return 'launcher'
        else:
            return 'system'
    
    def _auto_sender(self):
        """Thread que envía logs automáticamente"""
        while True:
            try:
                time.sleep(self.flush_interval)
                current_time = time.time()
                
                # Enviar si han pasado más de flush_interval segundos
                if current_time - self.last_flush >= self.flush_interval:
                    with self.buffer_lock:
                        if self.buffer:
                            self._flush_buffer()
                            
            except Exception as e:
                print(f"Error en auto_sender: {e}")
    
    def _flush_buffer(self):
        """Enviar logs del buffer al backend"""
        if not self.buffer:
            return
            
        try:
            # Enviar logs usando add_log
            for log_entry in self.buffer:
                self.web_sender.add_log(
                    level=log_entry['level'],
                    logger=log_entry['logger'],
                    message=log_entry['message'],
                    module=log_entry.get('module'),
                    function=log_entry.get('function'),
                    line=log_entry.get('line'),
                    component=log_entry.get('component'),
                    metadata=log_entry.get('metadata')
                )
            
            print(f"📤 Enviados {len(self.buffer)} logs al backend")
            self.buffer.clear()
            self.last_flush = time.time()
            
        except Exception as e:
            print(f"Error enviando logs al backend: {e}")
            # Mantener logs en buffer para retry
    
    def close(self):
        """Enviar logs pendientes antes de cerrar"""
        with self.buffer_lock:
            self._flush_buffer()
        super().close()


def setup_web_log_handler(web_sender):
    """Configurar el handler web para todos los loggers"""
    handler = WebLogHandler(web_sender)
    handler.setLevel(logging.INFO)
    
    # Configurar formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Agregar a logger raíz para capturar todos los logs
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    
    try:
        print("🔗 WebLogHandler configurado - todos los logs serán enviados al backend")
    except UnicodeEncodeError:
        print("[WebLogHandler] Configurado - todos los logs seran enviados al backend")
    return handler