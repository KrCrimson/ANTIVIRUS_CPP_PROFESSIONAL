"""
Health check API endpoints
=========================

Health monitoring and system status endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
import logging
import psutil
import os
from datetime import datetime, timedelta

from ..database import get_db, check_database_health
from ..models import LogEntry
from ..schemas import HealthCheckResponse
from ..config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Track application start time
APP_START_TIME = datetime.utcnow()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health check",
    description="Check the health status of the logging server and its dependencies"
)
async def health_check(db: AsyncSession = Depends(get_db)):
    """Comprehensive health check of the application and its dependencies"""
    
    try:
        # Check database connectivity
        db_status = "healthy"
        total_logs = 0
        
        try:
            # Test database connection
            await db.execute(text("SELECT 1"))
            
            # Get total log count
            count_query = select(func.count(LogEntry.id))
            result = await db.execute(count_query)
            total_logs = result.scalar() or 0
            
        except Exception as e:
            logger.error(f"❌ Database health check failed: {e}")
            db_status = f"unhealthy: {str(e)}"
        
        # Calculate uptime
        uptime_seconds = int((datetime.utcnow() - APP_START_TIME).total_seconds())
        
        # Determine overall status
        overall_status = "healthy" if db_status == "healthy" else "unhealthy"
        
        logger.info(f"🏥 Health check completed: {overall_status}")
        
        return HealthCheckResponse(
            status=overall_status,
            timestamp=datetime.utcnow(),
            version=settings.app_version,
            uptime_seconds=uptime_seconds,
            database_status=db_status,
            total_logs=total_logs
        )
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=datetime.utcnow(),
            version=settings.app_version,
            uptime_seconds=0,
            database_status=f"error: {str(e)}",
            total_logs=0
        )


@router.get(
    "/health/detailed",
    summary="Detailed health check",
    description="Comprehensive system health information including performance metrics"
)
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """Detailed health check with system metrics"""
    
    try:
        # Basic health info
        basic_health = await health_check(db)
        
        # System metrics (if psutil is available)
        system_metrics = {}
        try:
            # CPU and memory usage
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('.')
            
            system_metrics = {
                'cpu_usage_percent': round(cpu_percent, 2),
                'memory_usage_percent': round(memory.percent, 2),
                'memory_available_mb': round(memory.available / 1024 / 1024, 2),
                'disk_usage_percent': round(disk.percent, 2),
                'disk_free_gb': round(disk.free / 1024 / 1024 / 1024, 2)
            }
        except Exception as e:
            system_metrics = {'error': f"Unable to get system metrics: {str(e)}"}
        
        # Recent log activity
        log_activity = {}
        try:
            # Logs in last hour
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            recent_query = select(func.count(LogEntry.id)).where(
                LogEntry.timestamp >= one_hour_ago
            )
            result = await db.execute(recent_query)
            logs_last_hour = result.scalar() or 0
            
            # Logs by level in last hour
            level_query = select(
                LogEntry.level,
                func.count(LogEntry.id).label('count')
            ).where(
                LogEntry.timestamp >= one_hour_ago
            ).group_by(LogEntry.level)
            
            result = await db.execute(level_query)
            logs_by_level = {row.level: row.count for row in result}
            
            log_activity = {
                'logs_last_hour': logs_last_hour,
                'logs_by_level_last_hour': logs_by_level,
                'avg_logs_per_minute': round(logs_last_hour / 60, 2)
            }
            
        except Exception as e:
            log_activity = {'error': f"Unable to get log activity: {str(e)}"}
        
        # Database metrics
        db_metrics = {}
        try:
            # Table sizes (simplified for SQLite/PostgreSQL compatibility)
            if 'sqlite' in settings.database_url:
                # SQLite specific queries
                size_query = text("SELECT COUNT(*) as count FROM log_entries")
                result = await db.execute(size_query)
                db_metrics['log_entries_count'] = result.scalar()
            else:
                # PostgreSQL specific queries
                size_query = text("""
                    SELECT 
                        schemaname,
                        tablename,
                        attname,
                        n_distinct,
                        correlation
                    FROM pg_stats 
                    WHERE tablename = 'log_entries' 
                    LIMIT 5
                """)
                result = await db.execute(size_query)
                db_metrics['table_stats'] = [dict(row) for row in result]
            
        except Exception as e:
            db_metrics = {'error': f"Unable to get database metrics: {str(e)}"}
        
        logger.info("🔍 Detailed health check completed")
        
        return {
            'basic_health': basic_health.dict(),
            'system_metrics': system_metrics,
            'log_activity': log_activity,
            'database_metrics': db_metrics,
            'configuration': {
                'debug_mode': settings.debug,
                'max_log_entries': settings.max_log_entries,
                'rate_limit_requests': settings.rate_limit_requests,
                'cors_origins': settings.cors_origins
            },
            'timestamp': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Detailed health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Detailed health check failed: {str(e)}"
        )


@router.get(
    "/health/readiness",
    summary="Readiness probe",
    description="Kubernetes-style readiness probe"
)
async def readiness_probe():
    """Simple readiness probe for Kubernetes deployments"""
    
    try:
        # Check if database is reachable
        is_ready = await check_database_health()
        
        if is_ready:
            return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service not ready"
            )
            
    except Exception as e:
        logger.error(f"❌ Readiness probe failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not ready"
        )


@router.get(
    "/health/liveness",
    summary="Liveness probe",
    description="Kubernetes-style liveness probe"
)
async def liveness_probe():
    """Simple liveness probe for Kubernetes deployments"""
    
    # Basic liveness check - just return success if the app is running
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": int((datetime.utcnow() - APP_START_TIME).total_seconds())
    }


@router.get(
    "/health/startup",
    summary="Startup probe", 
    description="Kubernetes-style startup probe"
)
async def startup_probe():
    """Startup probe to indicate when the application has finished starting up"""
    
    try:
        # Check if application has been running for at least 10 seconds
        uptime = (datetime.utcnow() - APP_START_TIME).total_seconds()
        
        if uptime < 10:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Application still starting up"
            )
        
        # Verify database connectivity
        is_db_ready = await check_database_health()
        
        if not is_db_ready:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not ready"
            )
        
        return {
            "status": "started",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": int(uptime)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Startup probe failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Startup check failed"
        )