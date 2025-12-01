"""
Backend FastAPI para Vercel - Sistema de Logs del Antivirus
============================================================

Backend simplificado optimizado para despliegue en Vercel.
Recibe logs de múltiples instancias de antivirus con identificación única.
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import os
import json
import asyncpg
import asyncio
from contextlib import asynccontextmanager

# Variables de entorno
API_KEY = os.getenv("API_KEY_MASTER", "5n8nAQro47O7bA8cjJXzHJxeTmKNQ9OcqRDurA1Xk4Y")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_kE0K3SuXaGZU@ep-dawn-dust-ahynxkwf-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require")

# Función para obtener conexión a la base de datos
async def get_db_connection():
	try:
		conn = await asyncpg.connect(DATABASE_URL)
		return conn
	except Exception as e:
		print(f"Error conectando a PostgreSQL: {e}")
		raise

# Variable global para evitar múltiples inicializaciones
db_initialized = False

# Función para inicializar la base de datos (las tablas ya existen)
async def init_database():
	global db_initialized
	if db_initialized:
		return
		
	try:
		# Las tablas ya existen en PostgreSQL, solo marcamos como inicializado
		db_initialized = True
		print("Database initialization: Using existing schema")
		return
	except Exception as e:
		print(f"Error inicializando base de datos: {e}")
		raise

# Configuración
app = FastAPI(
	title="Antivirus Logs API",
	description="API para recibir y gestionar logs de múltiples instancias de antivirus",
	version="1.1.0"
)

# CORS para permitir requests desde el frontend
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # En producción, especifica dominios permitidos
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# =================== MODELOS ===================

class LogEntry(BaseModel):
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

# =================== FUNCIONES DE BASE DE DATOS ===================

async def get_db_stats():
	"""Obtiene estadísticas de la base de datos usando el esquema existente"""
	conn = await get_db_connection()
	try:
		# Inicializar base de datos si es necesario
		await init_database()
		
		# Usar el esquema existente
		total_logs = await conn.fetchval("SELECT COUNT(*) FROM log_entries")
		total_instances = await conn.fetchval("SELECT COUNT(*) FROM antivirus_clients") # Usar antivirus_clients
		active_instances = await conn.fetchval("SELECT COUNT(*) FROM antivirus_clients WHERE \"isActive\" = true")
		
		# Logs por nivel
		logs_by_level = await conn.fetch("SELECT level, COUNT(*) as count FROM log_entries GROUP BY level")
		logs_dict = {row['level']: row['count'] for row in logs_by_level}
		
		# Último log
		last_log = await conn.fetchrow("SELECT * FROM log_entries ORDER BY \"createdAt\" DESC LIMIT 1")
		
		return {
			"total_logs": total_logs,
			"total_instances": total_instances,
			"active_instances": active_instances,
			"logs_by_level": logs_dict,
			"last_log": dict(last_log) if last_log else None
		}
	except Exception as e:
		print(f"Error obteniendo estadísticas: {e}")
		return {
			"total_logs": 0,
			"total_instances": 0,
			"active_instances": 0,
			"logs_by_level": {},
			"last_log": None
		}
	finally:
		await conn.close()

# =================== ENDPOINTS ===================

@app.get("/")
async def root():
	"""Endpoint raíz"""
	return {
		"service": "Antivirus Logs API",
		"version": "1.1.0",
		"status": "running",
		"endpoints": {
			"health": "/api/health",
			"logs": "/api/logs",
			"instances": "/api/instances"
		}
	}

@app.get("/api/health")
async def health_check():
	"""Health check para Vercel"""
	try:
		stats = await get_db_stats()
		return {
			"status": "healthy",
			"timestamp": datetime.now().isoformat(),
			"database": "postgresql",
			"total_logs": stats["total_logs"],
			"total_instances": stats["total_instances"]
		}
	except Exception as e:
		return {
			"status": "degraded",
			"timestamp": datetime.now().isoformat(),
			"database": "error",
			"error": str(e)
		}

@app.post("/api/logs", response_model=LogResponse)
async def receive_log(
	log: LogEntry,
	api_key: str = Depends(verify_api_key)
):
	"""
	Recibe un log del antivirus
    
	- **timestamp**: Fecha y hora del log
	- **level**: Nivel de severidad
	- **component**: Componente que generó el log
	- **message**: Mensaje del log
	- **instance_id**: UUID único de la instancia (NUEVO)
	- **details**: Información adicional
	"""
	try:
		conn = await get_db_connection()
		try:
			# Inicializar base de datos si es necesario
			await init_database()
			
			# Insertar log usando el esquema existente
			log_id = await conn.fetchval("""
				INSERT INTO log_entries (
					"clientId", timestamp, level, logger, message, component, metadata, processed, "createdAt"
				) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
				RETURNING id
			""", 
				log.instance_id or "unknown",  # clientId
				datetime.fromisoformat(log.timestamp.replace('Z', '+00:00')) if 'Z' in log.timestamp else datetime.fromisoformat(log.timestamp),
				log.level,     # level
				log.component, # logger (usar component como logger)
				log.message,   # message
				log.component, # component
				json.dumps(log.details) if log.details else '{}',  # metadata como JSON
				False,         # processed
				datetime.now(timezone.utc)  # createdAt
			)
			
			# Actualizar last_seen de la instancia si existe (usar antivirus_clients)
			if log.instance_id:
				await conn.execute("""
					UPDATE antivirus_clients 
					SET "lastSeen" = $1, "updatedAt" = $1 
					WHERE "clientId" = $2
				""", datetime.now(timezone.utc), log.instance_id)
			
			return LogResponse(
				success=True,
				message="Log recibido exitosamente",
				log_id=str(log_id)
			)
		finally:
			await conn.close()
        
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error procesando log: {str(e)}")

@app.post("/api/instances")
async def register_instance(
	instance: InstanceRegistration,
	api_key: str = Depends(verify_api_key)
):
	"""
	Registra o actualiza una instancia de antivirus
    
	- **id**: UUID único de la instancia
	- **hostname**: Nombre del host
	- **os_info**: Sistema operativo
	- **antivirus_version**: Versión del antivirus
	- **status**: Estado (active/inactive)
	"""
	try:
		conn = await get_db_connection()
		try:
			# Inicializar base de datos si es necesario
			await init_database()
			
			# Insertar o actualizar instancia usando el esquema existente (antivirus_clients)
			result = await conn.fetchrow("""
				INSERT INTO antivirus_clients (
					id, "clientId", hostname, version, os, "lastSeen", "isActive", "createdAt", "updatedAt"
				) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
				ON CONFLICT ("clientId") DO UPDATE SET
					hostname = EXCLUDED.hostname,
					version = EXCLUDED.version,
					os = EXCLUDED.os,
					"lastSeen" = EXCLUDED."lastSeen",
					"isActive" = EXCLUDED."isActive",
					"updatedAt" = EXCLUDED."updatedAt"
				RETURNING *
			""", 
				instance.id,  # id
				instance.id,  # clientId (usar el mismo ID)
				instance.hostname or "Unknown",  # hostname
				instance.antivirus_version or "1.0.0",  # version
				instance.os_info or "Unknown",  # os
				datetime.now(timezone.utc),  # lastSeen
				instance.status == "active",  # isActive
				datetime.now(timezone.utc),  # createdAt
				datetime.now(timezone.utc)   # updatedAt
			)
			
			instance_data = dict(result)
			# Convertir timestamps a ISO format
			if 'createdAt' in instance_data and instance_data['createdAt']:
				instance_data['createdAt'] = instance_data['createdAt'].isoformat()
			if 'lastSeen' in instance_data and instance_data['lastSeen']:
				instance_data['lastSeen'] = instance_data['lastSeen'].isoformat()
			
			return {
				"success": True,
				"message": "Instancia registrada/actualizada exitosamente",
				"instance": instance_data
			}
		finally:
			await conn.close()
        
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error registrando instancia: {str(e)}")

@app.get("/api/logs")
async def get_logs(
	instance_id: Optional[str] = None,
	level: Optional[str] = None,
	limit: int = 100,
	api_key: str = Depends(verify_api_key)
):
	"""
	Obtiene logs con filtros opcionales
    
	- **instance_id**: Filtrar por instancia específica
	- **level**: Filtrar por nivel de log
	- **limit**: Número máximo de logs a retornar
	"""
	try:
		conn = await get_db_connection()
		try:
			# Inicializar base de datos si es necesario
			await init_database()
			
			# Construir query usando el esquema existente
			query = "SELECT * FROM log_entries WHERE 1=1"
			params = []
			param_count = 0
			
			if instance_id:
				param_count += 1
				query += f' AND "clientId" = ${param_count}'
				params.append(instance_id)
			
			if level:
				param_count += 1
				query += f" AND level = ${param_count}"
				params.append(level.upper())
			
			query += f' ORDER BY "createdAt" DESC LIMIT ${param_count + 1}'
			params.append(limit)
			
			rows = await conn.fetch(query, *params)
			logs = []
			for row in rows:
				log_dict = dict(row)
				# Convertir timestamps
				if 'timestamp' in log_dict and log_dict['timestamp']:
					log_dict['timestamp'] = log_dict['timestamp'].isoformat()
				if 'createdAt' in log_dict and log_dict['createdAt']:
					log_dict['createdAt'] = log_dict['createdAt'].isoformat()
				if 'received_at' in log_dict and log_dict['received_at']:
					log_dict['received_at'] = log_dict['received_at'].isoformat()
				# Parsear metadata JSON
				if log_dict.get('metadata'):
					log_dict['details'] = log_dict['metadata'] if isinstance(log_dict['metadata'], dict) else json.loads(log_dict['metadata'])
				logs.append(log_dict)
			
			return {
				"success": True,
				"total": len(logs),
				"logs": logs
			}
		finally:
			await conn.close()
        
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error obteniendo logs: {str(e)}")

@app.get("/api/instances")
async def get_instances(
	status: Optional[str] = None,
	api_key: str = Depends(verify_api_key)
):
	"""
	Obtiene todas las instancias registradas
    
	- **status**: Filtrar por estado (active/inactive)
	"""
	try:
		conn = await get_db_connection()
		try:
			# Inicializar base de datos si es necesario
			await init_database()
			
			# Usar antivirus_clients del esquema existente
			query = "SELECT * FROM antivirus_clients"
			params = []
			
			if status:
				# Convertir status a boolean para isActive
				is_active = status == "active"
				query += ' WHERE "isActive" = $1'
				params.append(is_active)
			
			query += ' ORDER BY "createdAt" DESC'
			
			rows = await conn.fetch(query, *params)
			instances = []
			for row in rows:
				instance_dict = dict(row)
				# Convertir timestamps
				if 'createdAt' in instance_dict and instance_dict['createdAt']:
					instance_dict['createdAt'] = instance_dict['createdAt'].isoformat()
				if 'lastSeen' in instance_dict and instance_dict['lastSeen']:
					instance_dict['lastSeen'] = instance_dict['lastSeen'].isoformat()
				if 'updatedAt' in instance_dict and instance_dict['updatedAt']:
					instance_dict['updatedAt'] = instance_dict['updatedAt'].isoformat()
				instances.append(instance_dict)
			
			return {
				"success": True,
				"total": len(instances),
				"instances": instances
			}
		finally:
			await conn.close()
        
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error obteniendo instancias: {str(e)}")

@app.get("/api/stats")
async def get_stats(api_key: str = Depends(verify_api_key)):
	"""Obtiene estadísticas del sistema"""
	try:
		stats = await get_db_stats()
		return {
			"success": True,
			"stats": stats
		}
        
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

# =================== MANEJO DE ERRORES ===================

# =================== MÉTRICAS AVANZADAS PARA DASHBOARD ===================
from collections import Counter, defaultdict

@app.get("/api/metrics")
async def get_advanced_metrics(api_key: str = Depends(verify_api_key)):
	"""Métricas avanzadas para dashboard: top procesos, patrones, detecciones por hora, errores por componente"""
	try:
		conn = await get_db_connection()
		try:
			await init_database()
			
			# Obtener logs desde PostgreSQL
			rows = await conn.fetch("SELECT * FROM log_entries ORDER BY \"createdAt\" DESC LIMIT 10000")
			
			# Top procesos sospechosos detectados (por mensaje y detalles)
			process_counter = Counter()
			pattern_counter = Counter()
			detections_by_hour = defaultdict(int)
			errors_by_component = Counter()
			warnings_by_component = Counter()
			detections_total = 0

			for row in rows:
				log = dict(row)
				# Detección de procesos sospechosos
				msg = log.get("message", "")
				details = log.get("metadata", {}) if log.get("metadata") else {}
				component = log.get("component", "")
				timestamp = str(log.get("timestamp", ""))
				level = log.get("level", "")

				# Ejemplo: [DETECTION] Proceso sospechoso detectado: opera.exe - patrón: capture
				if "[DETECTION] Proceso sospechoso detectado:" in msg:
					detections_total += 1
					# Extraer proceso y patrón
					try:
						proc_part = msg.split("detectado:")[1].split("- patrón:")[0].strip()
						pattern_part = msg.split("patrón:")[1].strip()
						process_counter[proc_part] += 1
						pattern_counter[pattern_part] += 1
					except Exception:
						pass
					# Agrupar por hora
					try:
						hour = timestamp[:13]  # 'YYYY-MM-DDTHH'
						detections_by_hour[hour] += 1
					except Exception:
						pass
				# Errores y warnings por componente
				if level == "ERROR":
					errors_by_component[component] += 1
				if level == "WARNING":
					warnings_by_component[component] += 1

			# Top procesos y patrones
			top_processes = process_counter.most_common(10)
			top_patterns = pattern_counter.most_common(10)
			detections_hourly = sorted(detections_by_hour.items())
			top_errors = errors_by_component.most_common(10)
			top_warnings = warnings_by_component.most_common(10)

			return {
				"success": True,
				"metrics": {
					"top_processes": top_processes,
					"top_patterns": top_patterns,
					"detections_hourly": detections_hourly,
					"detections_total": detections_total,
					"top_errors": top_errors,
					"top_warnings": top_warnings
				}
			}
		finally:
			await conn.close()
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error obteniendo métricas avanzadas: {str(e)}")

@app.exception_handler(404)
async def not_found_handler(request, exc):
	return {
		"success": False,
		"error": "Endpoint no encontrado",
		"path": str(request.url)
	}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
	return {
		"success": False,
		"error": "Error interno del servidor",
		"detail": str(exc)
	}

# =================== PUNTO DE ENTRADA ===================

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)

# Para Vercel, exportamos la aplicación
app_handler = app
