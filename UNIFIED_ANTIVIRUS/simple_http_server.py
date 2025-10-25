#!/usr/bin/env python3
"""
Servidor HTTP simple para recibir logs - Solo para pruebas
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
from datetime import datetime
from urllib.parse import urlparse
import os

class LogHandler(BaseHTTPRequestHandler):
    """Maneja las peticiones HTTP para logs"""
    
    def do_POST(self):
        """Maneja peticiones POST"""
        if self.path == '/api/recibir_logs':
            try:
                # Leer datos
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                print(f"LOG RECIBIDO de PC: {data.get('pc_id', 'unknown')}")
                print(f"Timestamp: {data.get('timestamp', 'unknown')}")
                print(f"Logs: {len(data.get('logs', []))}")
                
                # Procesar cada log
                for log in data.get('logs', []):
                    print(f"  - {log.get('level', 'INFO')}: {log.get('message', '')}")
                    if 'extra_data' in log:
                        print(f"    Datos extra: {log['extra_data']}")
                
                # Guardar en base de datos simple
                self.save_to_db(data)
                
                # Respuesta exitosa
                response = {
                    "status": "success",
                    "message": "Logs recibidos exitosamente",
                    "logs_procesados": len(data.get('logs', []))
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
                print(f"RESPUESTA ENVIADA: {response}")
                
            except Exception as e:
                print(f"ERROR procesando log: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """Maneja peticiones GET"""
        if self.path == '/' or self.path == '/dashboard':
            # Página simple de dashboard
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Monitor de Logs - Antivirus</title>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial; margin: 40px; background: #f5f5f5; }
                    .container { background: white; padding: 20px; border-radius: 8px; }
                    .status { padding: 10px; background: #d4edda; border-radius: 4px; margin: 20px 0; }
                    .log-entry { padding: 8px; margin: 5px 0; background: #e9ecef; border-radius: 4px; }
                    .info { color: #0066cc; }
                    .warning { color: #ff8800; }
                    .error { color: #cc0000; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📊 Monitor de Logs - Antivirus Profesional</h1>
                    <div class="status">
                        ✅ Servidor HTTP funcionando correctamente<br>
                        🕒 Iniciado: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """<br>
                        📡 API Endpoint: /api/recibir_logs<br>
                        📊 Puerto: 8888
                    </div>
                    
                    <h2>Estado del Sistema</h2>
                    <div class="log-entry">
                        <strong>✅ Sistema Operativo:</strong> Activo<br>
                        <strong>🔗 API HTTP:</strong> Disponible<br>
                        <strong>💾 Base de Datos:</strong> SQLite funcionando<br>
                        <strong>📝 Logs:</strong> Recibiendo automáticamente
                    </div>
                    
                    <h2>Prueba de Conectividad</h2>
                    <p>Para probar el envío de logs, usa:</p>
                    <pre style="background: #f8f9fa; padding: 10px; border-radius: 4px;">
POST http://localhost:8888/api/recibir_logs
Content-Type: application/json

{
  "pc_id": "TEST_PC",
  "timestamp": "2025-10-25T10:00:00",
  "logs": [
    {
      "timestamp": "2025-10-25T10:00:00",
      "level": "INFO",
      "message": "Prueba de log",
      "extra_data": {"test": true}
    }
  ]
}
                    </pre>
                </div>
            </body>
            </html>
            """
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def save_to_db(self, data):
        """Guarda logs en base de datos SQLite"""
        try:
            conn = sqlite3.connect('simple_logs.db')
            cursor = conn.cursor()
            
            # Crear tabla si no existe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY,
                    pc_id TEXT,
                    timestamp TEXT,
                    level TEXT,
                    message TEXT,
                    extra_data TEXT,
                    received_at TEXT
                )
            ''')
            
            # Insertar logs
            for log in data.get('logs', []):
                cursor.execute('''
                    INSERT INTO logs (pc_id, timestamp, level, message, extra_data, received_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    data.get('pc_id'),
                    log.get('timestamp'),
                    log.get('level'),
                    log.get('message'),
                    json.dumps(log.get('extra_data', {})),
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error guardando en DB: {e}")

def main():
    """Inicia el servidor simple"""
    port = 8888
    
    print("=" * 60)
    print("SERVIDOR HTTP SIMPLE - MONITOR DE LOGS ANTIVIRUS")
    print("=" * 60)
    print(f"Puerto: {port}")
    print(f"Dashboard: http://localhost:{port}")
    print(f"API: http://localhost:{port}/api/recibir_logs")
    print("Para detener: Ctrl+C")
    print("=" * 60)
    
    try:
        server = HTTPServer(('localhost', port), LogHandler)
        print(f"Servidor iniciado exitosamente en puerto {port}")
        print("Esperando logs...")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()