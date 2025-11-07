"""
Logs API endpoints
=================

REST API endpoints for log management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc, or_, and_
from sqlalchemy.orm import selectinload
from typing import Optional, List
import json
import logging
from datetime import datetime, timedelta

from ..database import get_db
from ..auth import require_write_permission, require_read_permission, check_rate_limit
from ..models import LogEntry, APIKey
from ..schemas import (
    LogEntryCreate, LogEntryResponse, LogQueryParams, LogQueryResponse,
    BulkLogCreate, BulkLogResponse
)
from ..config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/logs",
    response_model=LogEntryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new log entry",
    description="Submit a single log entry from the antivirus system"
)
async def create_log_entry(
    log_data: LogEntryCreate,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(require_write_permission),
    _rate_limit: APIKey = Depends(check_rate_limit)
):
    """Create a new log entry in the database"""
    
    try:
        # Convert Pydantic model to database model
        log_entry = LogEntry(
            timestamp=log_data.timestamp,
            level=log_data.level.value,
            component=log_data.component,
            message=log_data.message,
            source_host=log_data.source_host,
            source_process=log_data.source_process,
            extra_data=json.dumps(log_data.extra_data) if log_data.extra_data else None,
            cpu_usage=log_data.cpu_usage,
            memory_usage=log_data.memory_usage,
            threat_type=log_data.threat_type,
            confidence_score=log_data.confidence_score,
            severity=log_data.severity.value if log_data.severity else None
        )
        
        # Add to database
        db.add(log_entry)
        await db.commit()
        await db.refresh(log_entry)
        
        logger.info(f"✅ Log entry created: ID={log_entry.id}, Level={log_entry.level}, Component={log_entry.component}")
        
        # Convert to response model
        return LogEntryResponse.model_validate(log_entry.to_dict())
        
    except Exception as e:
        await db.rollback()
        logger.error(f"❌ Failed to create log entry: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create log entry: {str(e)}"
        )


@router.post(
    "/logs/bulk",
    response_model=BulkLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple log entries",
    description="Submit multiple log entries in a single request for better performance"
)
async def create_bulk_logs(
    bulk_data: BulkLogCreate,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(require_write_permission),
    _rate_limit: APIKey = Depends(check_rate_limit)
):
    """Create multiple log entries efficiently"""
    
    created_ids = []
    errors = []
    
    try:
        for i, log_data in enumerate(bulk_data.logs):
            try:
                log_entry = LogEntry(
                    timestamp=log_data.timestamp,
                    level=log_data.level.value,
                    component=log_data.component,
                    message=log_data.message,
                    source_host=log_data.source_host,
                    source_process=log_data.source_process,
                    extra_data=json.dumps(log_data.extra_data) if log_data.extra_data else None,
                    cpu_usage=log_data.cpu_usage,
                    memory_usage=log_data.memory_usage,
                    threat_type=log_data.threat_type,
                    confidence_score=log_data.confidence_score,
                    severity=log_data.severity.value if log_data.severity else None
                )
                
                db.add(log_entry)
                
            except Exception as e:
                errors.append(f"Log {i}: {str(e)}")
        
        # Commit all valid entries
        await db.commit()
        
        # Get created IDs (this is a simplified approach)
        created_count = len(bulk_data.logs) - len(errors)
        
        logger.info(f"✅ Bulk log creation: {created_count} created, {len(errors)} failed")
        
        return BulkLogResponse(
            created_count=created_count,
            failed_count=len(errors),
            errors=errors,
            created_ids=created_ids  # Would need more complex logic to get actual IDs
        )
        
    except Exception as e:
        await db.rollback()
        logger.error(f"❌ Bulk log creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bulk log creation failed: {str(e)}"
        )


@router.get(
    "/logs",
    response_model=LogQueryResponse,
    summary="Query log entries",
    description="Retrieve log entries with filtering, pagination, and search capabilities"
)
async def query_logs(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=500, description="Page size"),
    level: Optional[str] = Query(None, description="Filter by log level"),
    component: Optional[str] = Query(None, description="Filter by component"),
    source_host: Optional[str] = Query(None, description="Filter by source host"),
    threat_type: Optional[str] = Query(None, description="Filter by threat type"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    date_from: Optional[datetime] = Query(None, description="Start date"),
    date_to: Optional[datetime] = Query(None, description="End date"),
    search: Optional[str] = Query(None, description="Search in messages"),
    sort_by: str = Query("received_at", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(require_read_permission)
):
    """Query logs with advanced filtering and pagination"""
    
    try:
        # Build base query
        query = select(LogEntry)
        
        # Apply filters
        conditions = []
        
        if level:
            conditions.append(LogEntry.level == level.upper())
        
        if component:
            conditions.append(LogEntry.component.ilike(f"%{component}%"))
        
        if source_host:
            conditions.append(LogEntry.source_host.ilike(f"%{source_host}%"))
        
        if threat_type:
            conditions.append(LogEntry.threat_type.ilike(f"%{threat_type}%"))
        
        if severity:
            conditions.append(LogEntry.severity == severity.upper())
        
        if date_from:
            conditions.append(LogEntry.timestamp >= date_from)
        
        if date_to:
            conditions.append(LogEntry.timestamp <= date_to)
        
        if search:
            conditions.append(LogEntry.message.ilike(f"%{search}%"))
        
        # Apply all conditions
        if conditions:
            query = query.where(and_(*conditions))
        
        # Count total records
        count_query = select(func.count(LogEntry.id))
        if conditions:
            count_query = count_query.where(and_(*conditions))
        
        result = await db.execute(count_query)
        total = result.scalar()
        
        # Apply sorting
        sort_column = getattr(LogEntry, sort_by, LogEntry.received_at)
        if sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        # Apply pagination
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)
        
        # Execute query
        result = await db.execute(query)
        logs = result.scalars().all()
        
        # Calculate pagination info
        pages = (total + size - 1) // size
        has_next = page < pages
        has_prev = page > 1
        
        # Convert to response models
        log_responses = [LogEntryResponse.model_validate(log.to_dict()) for log in logs]
        
        logger.info(f"📊 Query executed: {len(logs)} logs returned, page {page}/{pages}")
        
        return LogQueryResponse(
            logs=log_responses,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev
        )
        
    except Exception as e:
        logger.error(f"❌ Log query failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Log query failed: {str(e)}"
        )


@router.get(
    "/logs/{log_id}",
    response_model=LogEntryResponse,
    summary="Get a specific log entry",
    description="Retrieve a single log entry by its ID"
)
async def get_log_entry(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(require_read_permission)
):
    """Get a specific log entry by ID"""
    
    try:
        query = select(LogEntry).where(LogEntry.id == log_id)
        result = await db.execute(query)
        log_entry = result.scalar_one_or_none()
        
        if not log_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Log entry with ID {log_id} not found"
            )
        
        logger.info(f"📄 Log entry retrieved: ID={log_id}")
        
        return LogEntryResponse.model_validate(log_entry.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get log entry {log_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve log entry: {str(e)}"
        )


@router.delete(
    "/logs/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a log entry",
    description="Delete a specific log entry (admin only)"
)
async def delete_log_entry(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(require_write_permission)
):
    """Delete a specific log entry"""
    
    try:
        query = select(LogEntry).where(LogEntry.id == log_id)
        result = await db.execute(query)
        log_entry = result.scalar_one_or_none()
        
        if not log_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Log entry with ID {log_id} not found"
            )
        
        await db.delete(log_entry)
        await db.commit()
        
        logger.info(f"🗑️ Log entry deleted: ID={log_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"❌ Failed to delete log entry {log_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete log entry: {str(e)}"
        )