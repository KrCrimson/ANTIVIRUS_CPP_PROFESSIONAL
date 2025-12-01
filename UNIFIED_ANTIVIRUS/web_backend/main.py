"""
Backend FastAPI para Vercel con PostgreSQL - Sistema de Logs del Antivirus
===========================================================================

Backend con almacenamiento persistente en PostgreSQL.
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import os

# Importar modelos de base de datos
try:
    from database import init_db, LogEntry as DBLogEntry, AntivirusInstance as DBInstance, get_db_session
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("WARNING: Database module not available, using in-memory storage")

# Configuración
app = FastAPI(
    title="Antivirus Logs API",
    description="API para recibir y gestionar logs de múltiples instancias de antivirus con PostgreSQL",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables de entorno
API_KEY = os.getenv("API_KEY_MASTER", "dev-key-12345")
DATABASE_URL = os.getenv("DATABASE_URL", None)

# Inicializar base de datos
engine, SessionLocal = None, None
if DB_AVAILABLE and DATABASE_URL:
    try:
        engine, SessionLocal = init_db()
        print(f"✅ PostgreSQL connected: {DATABASE_URL[:30]}...")
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        DB_AVAILABLE = False

# Fallback a almacenamiento en memoria si no hay DB
logs_storage: List[Dict[str, Any]] = []
instances_storage: Dict[str, Dict[str, Any]] = {}

# =================== MODELOS PYDANTIC ===================

class LogEntryModel(BaseModel):
    """Modelo para entrada de log"""
    timestamp: str = Field(..., description="Timestamp del log en formato ISO")
    level: str = Field(..., description="Nivel del log (INFO, WARNING, ERROR, etc.)")
    component: str = Field(..., description="Componente del antivirus que generó el log")
    message: str = Field(..., description="Mensaje del log")
    instance_id: Optional[str] = Field(None, description="UUID único de la instancia del antivirus")
    details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Detalles adicionales")

class InstanceRegistration(BaseModel):
    """Modelo para registro de instancia"""
    id: str = Field(..., description="UUID único de la instancia")
    hostname: Optional[str] = Field(None, description="Nombre del host")
    os_info: Optional[str] = Field(None, description="Información del sistema operativo")
    antivirus_version: Optional[str] = Field(None, description="Versión del antivirus")
    status: str = Field(default="active", description="Estado de la instancia")

class LogResponse(BaseModel):
    """Respuesta al recibir un log"""
    success: bool
    message: str
    log_id: Optional[str] = None

# =================== AUTENTICACIÓN ===================

async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    """Verifica la API key en el header"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")
    return x_api_key

# =================== ENDPOINTS ===================

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "service": "Antivirus Logs API",
        "version": "2.0.0",
        "status": "running",
        "storage": "PostgreSQL" if (DB_AVAILABLE and SessionLocal) else "in-memory",
        "endpoints": {
            "health": "/api/health",
            "logs": "/api/logs",
            "instances": "/api/instances"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check para Vercel"""
    storage_type = "PostgreSQL" if (DB_AVAILABLE and SessionLocal) else "in-memory"
    
    if DB_AVAILABLE and SessionLocal:
        try:
            db = get_db_session(SessionLocal)
            total_logs = db.query(DBLogEntry).count()
            total_instances = db.query(DBInstance).count()
            db.close()
        except Exception as e:
            return {
                "status": "degraded",
                "timestamp": datetime.utcnow().isoformat(),
                "database": "error",
                "error": str(e)
            }
    else:
        total_logs = len(logs_storage)
        total_instances = len(instances_storage)
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": storage_type,
        "total_logs": total_logs,
        "total_instances": total_instances
    }

@app.post("/api/logs", response_model=LogResponse)
async def receive_log(
    log: LogEntryModel,
    api_key: str = Depends(verify_api_key)
):
    """Recibe un log del antivirus y lo guarda en PostgreSQL"""
    try:
        if DB_AVAILABLE and SessionLocal:
            # Guardar en PostgreSQL
            db = get_db_session(SessionLocal)
            try:
                db_log = DBLogEntry(
                    timestamp=datetime.fromisoformat(log.timestamp.replace('Z', '+00:00')).replace(tzinfo=None),
                    level=log.level,
                    component=log.component,
                    message=log.message,
                    instance_id=log.instance_id,
                    details=log.details
                )
                db.add(db_log)
                db.commit()
                db.refresh(db_log)
                log_id = str(db_log.id)
                
                if log.instance_id:
                    instance = db.query(DBInstance).filter(DBInstance.id == log.instance_id).first()
                    if instance:
                        instance.last_seen = datetime.utcnow()
                        db.commit()
                
                db.close()
                return LogResponse(
                    success=True,
                    message="Log guardado en PostgreSQL",
                    log_id=log_id
                )
            except Exception as e:
                db.close()
                raise HTTPException(status_code=500, detail=f"Error guardando en DB: {str(e)}")
        else:
            # Fallback a memoria
            log_entry = {
                "id": f"log_{len(logs_storage) + 1}",
                "timestamp": log.timestamp,
                "level": log.level,
                "component": log.component,
                "message": log.message,
                "instance_id": log.instance_id,
                "details": log.details,
                "received_at": datetime.now().isoformat()
            }
            logs_storage.append(log_entry)
            
            if log.instance_id and log.instance_id in instances_storage:
                instances_storage[log.instance_id]["last_seen"] = datetime.now().isoformat()
            
            return LogResponse(
                success=True,
                message="Log guardado en memoria (PostgreSQL no disponible)",
                log_id=log_entry["id"]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando log: {str(e)}")

@app.post("/api/instances")
async def register_instance(
    instance: InstanceRegistration,
    api_key: str = Depends(verify_api_key)
):
    """Registra o actualiza una instancia de antivirus en PostgreSQL"""
    try:
        if DB_AVAILABLE and SessionLocal:
            # Guardar en PostgreSQL
            db = get_db_session(SessionLocal)
            try:
                existing = db.query(DBInstance).filter(DBInstance.id == instance.id).first()
                
                if existing:
                    # Actualizar
                    existing.hostname = instance.hostname
                    existing.os_info = instance.os_info
                    existing.antivirus_version = instance.antivirus_version
                    existing.status = instance.status
                    existing.last_seen = datetime.utcnow()
                    message = "Instancia actualizada en PostgreSQL"
                else:
                    # Crear nueva
                    db_instance = DBInstance(
                        id=instance.id,
                        hostname=instance.hostname,
                        os_info=instance.os_info,
                        antivirus_version=instance.antivirus_version,
                        status=instance.status
                    )
                    db.add(db_instance)
                    message = "Instancia registrada en PostgreSQL"
                
                db.commit()
                db.close()
                
                return {
                    "success": True,
                    "message": message,
                    "instance_id": instance.id
                }
            except Exception as e:
                db.close()
                raise HTTPException(status_code=500, detail=f"Error guardando instancia: {str(e)}")
        else:
            # Fallback a memoria
            is_new = instance.id not in instances_storage
            instance_data = {
                "id": instance.id,
                "hostname": instance.hostname,
                "os_info": instance.os_info,
                "antivirus_version": instance.antivirus_version,
                "status": instance.status,
                "last_seen": datetime.now().isoformat(),
                "created_at": instances_storage.get(instance.id, {}).get("created_at", datetime.now().isoformat())
            }
            instances_storage[instance.id] = instance_data
            
            return {
                "success": True,
                "message": "Instancia registrada en memoria" if is_new else "Instancia actualizada en memoria",
                "instance": instance_data
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando instancia: {str(e)}")

@app.get("/api/logs")
async def get_logs(
    instance_id: Optional[str] = None,
    level: Optional[str] = None,
    limit: int = 100,
    api_key: str = Depends(verify_api_key)
):
    """Obtiene logs desde PostgreSQL con filtros opcionales"""
    try:
        if DB_AVAILABLE and SessionLocal:
            db = get_db_session(SessionLocal)
            try:
                query = db.query(DBLogEntry)
                
                if instance_id:
                    query = query.filter(DBLogEntry.instance_id == instance_id)
                if level:
                    query = query.filter(DBLogEntry.level == level.upper())
                
                query = query.order_by(DBLogEntry.received_at.desc()).limit(limit)
                logs = query.all()
                
                result = [{
                    "id": log.id,
                    "timestamp": log.timestamp.isoformat(),
                    "level": log.level,
                    "component": log.component,
                    "message": log.message,
                    "instance_id": log.instance_id,
                    "details": log.details,
                    "received_at": log.received_at.isoformat()
                } for log in logs]
                
                db.close()
                return {"success": True, "total": len(result), "logs": result}
            except Exception as e:
                db.close()
                raise HTTPException(status_code=500, detail=f"Error obteniendo logs: {str(e)}")
        else:
            # Fallback a memoria
            filtered_logs = logs_storage.copy()
            if instance_id:
                filtered_logs = [log for log in filtered_logs if log.get("instance_id") == instance_id]
            if level:
                filtered_logs = [log for log in filtered_logs if log.get("level") == level.upper()]
            filtered_logs = filtered_logs[-limit:]
            
            return {"success": True, "total": len(filtered_logs), "logs": filtered_logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo logs: {str(e)}")

@app.get("/api/instances")
async def get_instances(
    status: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    """Obtiene instancias desde PostgreSQL"""
    try:
        if DB_AVAILABLE and SessionLocal:
            db = get_db_session(SessionLocal)
            try:
                query = db.query(DBInstance)
                if status:
                    query = query.filter(DBInstance.status == status)
                
                instances = query.all()
                result = [{
                    "id": inst.id,
                    "hostname": inst.hostname,
                    "os_info": inst.os_info,
                    "antivirus_version": inst.antivirus_version,
                    "status": inst.status,
                    "last_seen": inst.last_seen.isoformat(),
                    "created_at": inst.created_at.isoformat()
                } for inst in instances]
                
                db.close()
                return {"success": True, "total": len(result), "instances": result}
            except Exception as e:
                db.close()
                raise HTTPException(status_code=500, detail=f"Error obteniendo instancias: {str(e)}")
        else:
            # Fallback a memoria
            instances = list(instances_storage.values())
            if status:
                instances = [inst for inst in instances if inst.get("status") == status]
            return {"success": True, "total": len(instances), "instances": instances}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo instancias: {str(e)}")

@app.get("/api/stats")
async def get_stats(api_key: str = Depends(verify_api_key)):
    """Obtiene estadísticas desde PostgreSQL"""
    try:
        if DB_AVAILABLE and SessionLocal:
            db = get_db_session(SessionLocal)
            try:
                from sqlalchemy import func
                
                total_logs = db.query(DBLogEntry).count()
                total_instances = db.query(DBInstance).count()
                active_instances = db.query(DBInstance).filter(DBInstance.status == "active").count()
                
                # Logs por nivel
                log_levels = db.query(
                    DBLogEntry.level,
                    func.count(DBLogEntry.id)
                ).group_by(DBLogEntry.level).all()
                
                logs_by_level = {level: count for level, count in log_levels}
                
                # Último log
                last_log = db.query(DBLogEntry).order_by(DBLogEntry.received_at.desc()).first()
                last_log_data = None
                if last_log:
                    last_log_data = {
                        "timestamp": last_log.timestamp.isoformat(),
                        "level": last_log.level,
                        "message": last_log.message,
                        "received_at": last_log.received_at.isoformat()
                    }
                
                db.close()
                
                return {
                    "success": True,
                    "stats": {
                        "total_logs": total_logs,
                        "total_instances": total_instances,
                        "active_instances": active_instances,
                        "logs_by_level": logs_by_level,
                        "last_log": last_log_data
                    }
                }
            except Exception as e:
                db.close()
                raise HTTPException(status_code=500, detail=f"Error obteniendo stats: {str(e)}")
        else:
            # Fallback a memoria
            log_levels = {}
            for log in logs_storage:
                level = log.get("level", "UNKNOWN")
                log_levels[level] = log_levels.get(level, 0) + 1
            
            active_instances = sum(1 for inst in instances_storage.values() if inst.get("status") == "active")
            
            return {
                "success": True,
                "stats": {
                    "total_logs": len(logs_storage),
                    "total_instances": len(instances_storage),
                    "active_instances": active_instances,
                    "logs_by_level": log_levels,
                    "last_log": logs_storage[-1] if logs_storage else None
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
