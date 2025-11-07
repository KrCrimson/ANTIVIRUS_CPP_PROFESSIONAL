"""
Statistics API endpoints
=======================

Endpoints for log statistics and analytics
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime, timedelta

from ..database import get_db
from ..auth import require_read_permission
from ..models import LogEntry, APIKey
from ..schemas import LogStatisticsResponse
from ..config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/stats",
    response_model=LogStatisticsResponse,
    summary="Get log statistics",
    description="Retrieve comprehensive statistics about stored logs"
)
async def get_log_statistics(
    hours: int = Query(24, ge=1, le=168, description="Time window in hours"),
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(require_read_permission)
):
    """Get comprehensive log statistics for the specified time window"""
    
    try:
        # Calculate time window
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        # Base query for time window
        base_query = select(LogEntry).where(
            and_(
                LogEntry.timestamp >= start_time,
                LogEntry.timestamp <= end_time
            )
        )
        
        # Total logs count
        count_query = select(func.count(LogEntry.id)).where(
            and_(
                LogEntry.timestamp >= start_time,
                LogEntry.timestamp <= end_time
            )
        )
        result = await db.execute(count_query)
        total_logs = result.scalar() or 0
        
        # Logs by level
        level_query = select(
            LogEntry.level,
            func.count(LogEntry.id).label('count')
        ).where(
            and_(
                LogEntry.timestamp >= start_time,
                LogEntry.timestamp <= end_time
            )
        ).group_by(LogEntry.level)
        
        result = await db.execute(level_query)
        logs_by_level = {row.level: row.count for row in result}
        
        # Logs by component
        component_query = select(
            LogEntry.component,
            func.count(LogEntry.id).label('count')
        ).where(
            and_(
                LogEntry.timestamp >= start_time,
                LogEntry.timestamp <= end_time
            )
        ).group_by(LogEntry.component).order_by(desc('count')).limit(10)
        
        result = await db.execute(component_query)
        logs_by_component = {row.component: row.count for row in result}
        
        # Hourly timeline
        logs_by_hour = []
        current_hour = start_time.replace(minute=0, second=0, microsecond=0)
        
        while current_hour <= end_time:
            next_hour = current_hour + timedelta(hours=1)
            
            hour_query = select(func.count(LogEntry.id)).where(
                and_(
                    LogEntry.timestamp >= current_hour,
                    LogEntry.timestamp < next_hour
                )
            )
            result = await db.execute(hour_query)
            count = result.scalar() or 0
            
            logs_by_hour.append({
                'hour': current_hour.isoformat(),
                'count': count
            })
            
            current_hour = next_hour
        
        # Threat statistics
        threat_query = select(func.count(LogEntry.id)).where(
            and_(
                LogEntry.timestamp >= start_time,
                LogEntry.timestamp <= end_time,
                LogEntry.threat_type.isnot(None)
            )
        )
        result = await db.execute(threat_query)
        threats_detected = result.scalar() or 0
        
        # Average confidence for threats
        confidence_query = select(func.avg(LogEntry.confidence_score)).where(
            and_(
                LogEntry.timestamp >= start_time,
                LogEntry.timestamp <= end_time,
                LogEntry.confidence_score.isnot(None)
            )
        )
        result = await db.execute(confidence_query)
        avg_confidence = result.scalar()
        
        # Critical threats
        critical_query = select(func.count(LogEntry.id)).where(
            and_(
                LogEntry.timestamp >= start_time,
                LogEntry.timestamp <= end_time,
                LogEntry.severity == 'CRITICAL'
            )
        )
        result = await db.execute(critical_query)
        critical_threats = result.scalar() or 0
        
        # Top components with activity
        top_components_query = select(
            LogEntry.component,
            func.count(LogEntry.id).label('count'),
            func.avg(LogEntry.cpu_usage).label('avg_cpu'),
            func.avg(LogEntry.memory_usage).label('avg_memory')
        ).where(
            and_(
                LogEntry.timestamp >= start_time,
                LogEntry.timestamp <= end_time
            )
        ).group_by(LogEntry.component).order_by(desc('count')).limit(5)
        
        result = await db.execute(top_components_query)
        top_components = []
        for row in result:
            top_components.append({
                'component': row.component,
                'log_count': row.count,
                'avg_cpu_usage': round(row.avg_cpu, 2) if row.avg_cpu else None,
                'avg_memory_usage': round(row.avg_memory, 2) if row.avg_memory else None
            })
        
        logger.info(f"📊 Statistics generated for {hours}h window: {total_logs} total logs")
        
        return LogStatisticsResponse(
            total_logs=total_logs,
            logs_by_level=logs_by_level,
            logs_by_component=logs_by_component,
            logs_by_hour=logs_by_hour,
            threats_detected=threats_detected,
            avg_confidence=round(avg_confidence, 3) if avg_confidence else None,
            critical_threats=critical_threats,
            top_components=top_components,
            date_range={
                'start': start_time,
                'end': end_time
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Statistics generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate statistics: {str(e)}"
        )


@router.get(
    "/stats/timeline",
    summary="Get timeline statistics",
    description="Get log counts over time with configurable granularity"
)
async def get_timeline_stats(
    hours: int = Query(24, ge=1, le=168, description="Time window in hours"),
    granularity: str = Query("hour", pattern="^(hour|day)$", description="Time granularity"),
    level: Optional[str] = Query(None, description="Filter by log level"),
    component: Optional[str] = Query(None, description="Filter by component"),
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(require_read_permission)
):
    """Get timeline statistics with flexible granularity and filtering"""
    
    try:
        # Calculate time window
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        # Determine time bucket size
        if granularity == "hour":
            bucket_size = timedelta(hours=1)
        else:  # day
            bucket_size = timedelta(days=1)
        
        # Build base conditions
        conditions = [
            LogEntry.timestamp >= start_time,
            LogEntry.timestamp <= end_time
        ]
        
        if level:
            conditions.append(LogEntry.level == level.upper())
        
        if component:
            conditions.append(LogEntry.component.ilike(f"%{component}%"))
        
        # Generate timeline
        timeline = []
        current_time = start_time.replace(minute=0, second=0, microsecond=0)
        
        if granularity == "day":
            current_time = current_time.replace(hour=0)
        
        while current_time <= end_time:
            next_time = current_time + bucket_size
            
            # Query for this time bucket
            bucket_conditions = conditions + [
                LogEntry.timestamp >= current_time,
                LogEntry.timestamp < next_time
            ]
            
            query = select(func.count(LogEntry.id)).where(and_(*bucket_conditions))
            result = await db.execute(query)
            count = result.scalar() or 0
            
            timeline.append({
                'timestamp': current_time.isoformat(),
                'count': count,
                'period': granularity
            })
            
            current_time = next_time
        
        logger.info(f"📈 Timeline generated: {len(timeline)} {granularity} buckets")
        
        return {
            'timeline': timeline,
            'granularity': granularity,
            'total_periods': len(timeline),
            'filters': {
                'level': level,
                'component': component,
                'hours': hours
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Timeline generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate timeline: {str(e)}"
        )


@router.get(
    "/stats/threats",
    summary="Get threat statistics",
    description="Get detailed statistics about detected threats"
)
async def get_threat_statistics(
    hours: int = Query(24, ge=1, le=168, description="Time window in hours"),
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(require_read_permission)
):
    """Get detailed threat detection statistics"""
    
    try:
        # Calculate time window
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        # Base conditions for threats
        threat_conditions = [
            LogEntry.timestamp >= start_time,
            LogEntry.timestamp <= end_time,
            LogEntry.threat_type.isnot(None)
        ]
        
        # Total threats
        total_query = select(func.count(LogEntry.id)).where(and_(*threat_conditions))
        result = await db.execute(total_query)
        total_threats = result.scalar() or 0
        
        # Threats by type
        type_query = select(
            LogEntry.threat_type,
            func.count(LogEntry.id).label('count'),
            func.avg(LogEntry.confidence_score).label('avg_confidence')
        ).where(
            and_(*threat_conditions)
        ).group_by(LogEntry.threat_type).order_by(desc('count'))
        
        result = await db.execute(type_query)
        threats_by_type = []
        for row in result:
            threats_by_type.append({
                'threat_type': row.threat_type,
                'count': row.count,
                'avg_confidence': round(row.avg_confidence, 3) if row.avg_confidence else None
            })
        
        # Threats by severity
        severity_query = select(
            LogEntry.severity,
            func.count(LogEntry.id).label('count')
        ).where(
            and_(*threat_conditions)
        ).group_by(LogEntry.severity).order_by(desc('count'))
        
        result = await db.execute(severity_query)
        threats_by_severity = {row.severity or 'UNKNOWN': row.count for row in result}
        
        # High confidence threats (>0.8)
        high_confidence_query = select(func.count(LogEntry.id)).where(
            and_(
                *threat_conditions,
                LogEntry.confidence_score > 0.8
            )
        )
        result = await db.execute(high_confidence_query)
        high_confidence_threats = result.scalar() or 0
        
        # Recent critical threats
        recent_critical_query = select(
            LogEntry.timestamp,
            LogEntry.threat_type,
            LogEntry.confidence_score,
            LogEntry.component,
            LogEntry.message
        ).where(
            and_(
                LogEntry.timestamp >= start_time,
                LogEntry.timestamp <= end_time,
                LogEntry.severity == 'CRITICAL'
            )
        ).order_by(desc(LogEntry.timestamp)).limit(10)
        
        result = await db.execute(recent_critical_query)
        recent_critical = []
        for row in result:
            recent_critical.append({
                'timestamp': row.timestamp.isoformat(),
                'threat_type': row.threat_type,
                'confidence': row.confidence_score,
                'component': row.component,
                'message': row.message[:100] + '...' if len(row.message) > 100 else row.message
            })
        
        logger.info(f"🔍 Threat statistics generated: {total_threats} threats in {hours}h")
        
        return {
            'total_threats': total_threats,
            'threats_by_type': threats_by_type,
            'threats_by_severity': threats_by_severity,
            'high_confidence_threats': high_confidence_threats,
            'recent_critical_threats': recent_critical,
            'time_window_hours': hours,
            'confidence_threshold': 0.8
        }
        
    except Exception as e:
        logger.error(f"❌ Threat statistics failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate threat statistics: {str(e)}"
        )