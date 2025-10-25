"""
Web Monitor Server - Servidor web para recibir y gestionar logs del antivirus
============================================================================

Este servidor recibe logs de múltiples PCs con el antivirus instalado
y proporciona APIs para visualización y análisis de datos.
"""

# Imports con manejo de errores para dependencias opcionales
try:
    from fastapi import FastAPI, HTTPException, Depends, Request
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.security import HTTPBasic, HTTPBasicCredentials
    import uvicorn
    from pydantic import BaseModel, Field
    FASTAPI_AVAILABLE = True
except ImportError as e:
    print(f"ADVERTENCIA - FastAPI no disponible: {e}")
    print("📦 Instale las dependencias: pip install -r requirements_web_monitor.txt")
    FASTAPI_AVAILABLE = False
    
    # Clases mock para desarrollo sin FastAPI
    class FastAPI:
        def __init__(self, **kwargs): pass
        def get(self, path): return lambda func: func
        def post(self, path): return lambda func: func
        def add_middleware(self, *args, **kwargs): pass
        def mount(self, *args, **kwargs): pass
    
    class BaseModel:
        def __init__(self, **kwargs): 
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    def Depends(func): return func
    HTTPException = Exception
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import sqlite3
import os
import hashlib
import logging
from pathlib import Path
import secrets
from collections import defaultdict, Counter
import pandas as pd

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelos de datos
class LogEntry(BaseModel):
    pc_id: str
    timestamp: str
    level: str
    logger: str
    message: str
    source_file: str
    raw_log: str
    parsed: bool

class PCInfo(BaseModel):
    hostname: str
    platform: str
    processor: str
    python_version: str
    ip_address: str

class BatchInfo(BaseModel):
    count: int
    timestamp: str
    checksum: str

class LogBatch(BaseModel):
    pc_id: str
    pc_info: PCInfo
    logs: List[LogEntry]
    batch_info: BatchInfo

class MetricsResponse(BaseModel):
    total_logs: int
    active_pcs: int
    log_levels: Dict[str, int]
    recent_activity: List[Dict[str, Any]]
    top_loggers: List[Dict[str, Any]]

# Base de datos
class DatabaseManager:
    """Gestor de base de datos SQLite para almacenar logs"""
    
    def __init__(self, db_path: str = "web_monitor.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa las tablas de la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de PCs registradas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pcs (
                pc_id TEXT PRIMARY KEY,
                hostname TEXT,
                platform TEXT,
                processor TEXT,
                python_version TEXT,
                ip_address TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pc_id TEXT,
                timestamp TEXT,
                level TEXT,
                logger TEXT,
                message TEXT,
                source_file TEXT,
                raw_log TEXT,
                parsed BOOLEAN,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pc_id) REFERENCES pcs (pc_id)
            )
        ''')
        
        # Tabla de batches recibidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS batches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pc_id TEXT,
                batch_count INTEGER,
                batch_timestamp TEXT,
                checksum TEXT,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pc_id) REFERENCES pcs (pc_id)
            )
        ''')
        
        # Índices para mejorar rendimiento
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_pc_id ON logs(pc_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_received_at ON logs(received_at)')
        
        conn.commit()
        conn.close()
    
    def register_pc(self, pc_id: str, pc_info: PCInfo):
        """Registra o actualiza información de una PC"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO pcs 
            (pc_id, hostname, platform, processor, python_version, ip_address, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (pc_id, pc_info.hostname, pc_info.platform, 
              pc_info.processor, pc_info.python_version, pc_info.ip_address))
        
        conn.commit()
        conn.close()
    
    def store_logs(self, logs: List[LogEntry]):
        """Almacena logs en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        log_data = [
            (log.pc_id, log.timestamp, log.level, log.logger, 
             log.message, log.source_file, log.raw_log, log.parsed)
            for log in logs
        ]
        
        cursor.executemany('''
            INSERT INTO logs 
            (pc_id, timestamp, level, logger, message, source_file, raw_log, parsed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', log_data)
        
        conn.commit()
        conn.close()
    
    def store_batch_info(self, pc_id: str, batch_info: BatchInfo):
        """Almacena información del batch recibido"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO batches (pc_id, batch_count, batch_timestamp, checksum)
            VALUES (?, ?, ?, ?)
        ''', (pc_id, batch_info.count, batch_info.timestamp, batch_info.checksum))
        
        conn.commit()
        conn.close()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas generales del sistema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total de logs
        cursor.execute('SELECT COUNT(*) FROM logs')
        total_logs = cursor.fetchone()[0]
        
        # PCs activas (que han enviado logs en las últimas 24 horas)
        cursor.execute('''
            SELECT COUNT(DISTINCT pc_id) FROM logs 
            WHERE received_at > datetime('now', '-24 hours')
        ''')
        active_pcs = cursor.fetchone()[0]
        
        # Distribución por nivel de log
        cursor.execute('SELECT level, COUNT(*) FROM logs GROUP BY level')
        log_levels = dict(cursor.fetchall())
        
        # Actividad reciente (últimas 24 horas por hora)
        cursor.execute('''
            SELECT strftime('%Y-%m-%d %H:00:00', received_at) as hour, COUNT(*) as count
            FROM logs 
            WHERE received_at > datetime('now', '-24 hours')
            GROUP BY hour 
            ORDER BY hour
        ''')
        recent_activity = [{"hour": row[0], "count": row[1]} for row in cursor.fetchall()]
        
        # Top loggers
        cursor.execute('''
            SELECT logger, COUNT(*) as count FROM logs 
            WHERE received_at > datetime('now', '-24 hours')
            GROUP BY logger 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        top_loggers = [{"logger": row[0], "count": row[1]} for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "total_logs": total_logs,
            "active_pcs": active_pcs,
            "log_levels": log_levels,
            "recent_activity": recent_activity,
            "top_loggers": top_loggers
        }
    
    def get_pcs(self) -> List[Dict[str, Any]]:
        """Obtiene lista de PCs registradas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT pc_id, hostname, platform, processor, python_version, 
                   ip_address, first_seen, last_seen,
                   (SELECT COUNT(*) FROM logs WHERE logs.pc_id = pcs.pc_id) as total_logs
            FROM pcs 
            ORDER BY last_seen DESC
        ''')
        
        columns = ['pc_id', 'hostname', 'platform', 'processor', 'python_version',
                  'ip_address', 'first_seen', 'last_seen', 'total_logs']
        
        pcs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        
        return pcs
    
    def get_logs(self, pc_id: Optional[str] = None, level: Optional[str] = None,
                limit: int = 1000, offset: int = 0) -> List[Dict[str, Any]]:
        """Obtiene logs con filtros opcionales"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM logs WHERE 1=1'
        params = []
        
        if pc_id:
            query += ' AND pc_id = ?'
            params.append(pc_id)
        
        if level:
            query += ' AND level = ?'
            params.append(level)
        
        query += ' ORDER BY received_at DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        
        columns = [desc[0] for desc in cursor.description]
        logs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return logs

# Inicializar componentes
app = FastAPI(
    title="Antivirus Web Monitor",
    description="Sistema de monitoreo web para logs del antivirus unificado",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gestor de base de datos
db = DatabaseManager()

# Autenticación básica (cambiar credenciales en producción)
security = HTTPBasic()
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "antivirus2025"  # Cambiar en producción

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verifica credenciales de administrador"""
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Configurar templates y archivos estáticos
templates = Jinja2Templates(directory="web_templates")
os.makedirs("web_static", exist_ok=True)
app.mount("/static", StaticFiles(directory="web_static"), name="static")

# Endpoints de la API

@app.post("/api/recibir_logs")
async def recibir_logs(batch: LogBatch):
    """Endpoint para recibir logs desde las PCs clientes"""
    try:
        # Verificar checksum del batch
        expected_checksum = hashlib.md5(
            json.dumps([log.dict() for log in batch.logs], sort_keys=True).encode()
        ).hexdigest()
        
        if batch.batch_info.checksum != expected_checksum:
            raise HTTPException(
                status_code=400,
                detail="Checksum inválido"
            )
        
        # Registrar PC
        db.register_pc(batch.pc_id, batch.pc_info)
        
        # Almacenar logs
        db.store_logs(batch.logs)
        
        # Almacenar info del batch
        db.store_batch_info(batch.pc_id, batch.batch_info)
        
        logger.info(f"Recibidos {len(batch.logs)} logs de PC {batch.pc_id}")
        
        return {
            "status": "success",
            "message": f"Recibidos {len(batch.logs)} logs correctamente",
            "pc_id": batch.pc_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error procesando logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metrics")
async def get_metrics(admin: str = Depends(verify_credentials)) -> MetricsResponse:
    """Obtiene métricas generales del sistema"""
    try:
        metrics = db.get_metrics()
        return MetricsResponse(**metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pcs")
async def get_pcs(admin: str = Depends(verify_credentials)):
    """Obtiene lista de PCs registradas"""
    try:
        return db.get_pcs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs")
async def get_logs(
    pc_id: Optional[str] = None,
    level: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    admin: str = Depends(verify_credentials)
):
    """Obtiene logs con filtros opcionales"""
    try:
        return db.get_logs(pc_id=pc_id, level=level, limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Dashboard web
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, admin: str = Depends(verify_credentials)):
    """Página principal del dashboard"""
    try:
        metrics = db.get_metrics()
        pcs = db.get_pcs()
        recent_logs = db.get_logs(limit=20)
        
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "metrics": metrics,
            "pcs": pcs,
            "recent_logs": recent_logs,
            "admin_user": admin
        })
    except Exception as e:
        logger.error(f"Error en dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pcs", response_class=HTMLResponse)
async def pcs_page(request: Request, admin: str = Depends(verify_credentials)):
    """Página de gestión de PCs"""
    try:
        pcs = db.get_pcs()
        return templates.TemplateResponse("pcs.html", {
            "request": request,
            "pcs": pcs,
            "admin_user": admin
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs", response_class=HTMLResponse)
async def logs_page(request: Request, admin: str = Depends(verify_credentials)):
    """Página de visualización de logs"""
    try:
        return templates.TemplateResponse("logs.html", {
            "request": request,
            "admin_user": admin
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Función principal que maneja la disponibilidad de dependencias"""
    if not FASTAPI_AVAILABLE:
        print("ERROR - No se pueden iniciar el servidor web sin las dependencias necesarias")
        print("📦 Para instalar las dependencias, ejecute:")
        print("   python setup_web_monitoring.py")
        print("   o")
        print("   pip install -r requirements_web_monitor.txt")
        return 1
    
    print("Iniciando servidor de monitoreo web...")
    print(f"Dashboard: http://localhost:8888")
    print(f"Usuario: {ADMIN_USERNAME}")
    print(f"Contraseña: {ADMIN_PASSWORD}")
    print("API: http://localhost:8888/docs")
    print()
    print("Para detener el servidor, presione Ctrl+C")
    
    try:
        uvicorn.run(
            "web_monitor_server:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"Error iniciando servidor: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())