"""
Routes for managing Antivirus Instances
========================================

Endpoints for registering, updating and querying antivirus instances
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime
from typing import List, Optional
import uuid

from ..database import get_db
from ..models import AntivirusInstance, LogEntry
from ..schemas import (
    AntivirusInstanceCreate,
    AntivirusInstanceUpdate,
    AntivirusInstanceResponse,
    ErrorResponse
)
from ..auth import verify_api_key

router = APIRouter()


@router.post(
    "/instances",
    response_model=AntivirusInstanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register or update an antivirus instance",
    description="Register a new instance or update existing one. Call this on first startup and periodically to update 'last_seen'."
)
async def register_instance(
    instance_data: AntivirusInstanceCreate,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Register or update an antivirus instance.
    
    If instance ID already exists, updates it with new data (upsert pattern).
    This allows clients to send their ID on every startup/log submission.
    """
    
    # Check if instance exists
    result = await db.execute(
        select(AntivirusInstance).where(AntivirusInstance.id == instance_data.id)
    )
    existing_instance = result.scalar_one_or_none()
    
    if existing_instance:
        # Update existing instance
        for key, value in instance_data.dict(exclude_unset=True, exclude={'id'}).items():
            if value is not None:
                if key == 'metadata' and isinstance(value, dict):
                    import json
                    setattr(existing_instance, key, json.dumps(value))
                else:
                    setattr(existing_instance, key, value)
        
        # Always update last_seen
        existing_instance.last_seen = datetime.utcnow()
        existing_instance.status = "active"
        
        await db.commit()
        await db.refresh(existing_instance)
        
        # Get log count
        log_count_result = await db.execute(
            select(func.count(LogEntry.id)).where(LogEntry.instance_id == existing_instance.id)
        )
        log_count = log_count_result.scalar()
        
        response_dict = existing_instance.to_dict()
        response_dict['log_count'] = log_count
        
        return AntivirusInstanceResponse(**response_dict)
    
    else:
        # Create new instance
        import json
        new_instance = AntivirusInstance(
            id=instance_data.id,
            hostname=instance_data.hostname,
            os_info=instance_data.os_info,
            antivirus_version=instance_data.antivirus_version,
            ip_address=instance_data.ip_address,
            mac_address=instance_data.mac_address,
            install_date=instance_data.install_date,
            metadata=json.dumps(instance_data.metadata) if instance_data.metadata else None,
            last_seen=datetime.utcnow(),
            status="active"
        )
        
        db.add(new_instance)
        await db.commit()
        await db.refresh(new_instance)
        
        response_dict = new_instance.to_dict()
        response_dict['log_count'] = 0
        
        return AntivirusInstanceResponse(**response_dict)


@router.get(
    "/instances",
    response_model=List[AntivirusInstanceResponse],
    summary="List all antivirus instances",
    description="Get list of all registered antivirus instances with optional filtering"
)
async def list_instances(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    skip: int = Query(0, ge=0, description="Number of results to skip"),
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """List all registered antivirus instances"""
    
    query = select(AntivirusInstance)
    
    if status:
        query = query.where(AntivirusInstance.status == status)
    
    query = query.order_by(desc(AntivirusInstance.last_seen)).limit(limit).offset(skip)
    
    result = await db.execute(query)
    instances = result.scalars().all()
    
    # Add log counts
    response_list = []
    for instance in instances:
        log_count_result = await db.execute(
            select(func.count(LogEntry.id)).where(LogEntry.instance_id == instance.id)
        )
        log_count = log_count_result.scalar()
        
        instance_dict = instance.to_dict()
        instance_dict['log_count'] = log_count
        response_list.append(AntivirusInstanceResponse(**instance_dict))
    
    return response_list


@router.get(
    "/instances/{instance_id}",
    response_model=AntivirusInstanceResponse,
    summary="Get instance by ID",
    description="Get detailed information about a specific instance"
)
async def get_instance(
    instance_id: str,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Get instance by ID"""
    
    result = await db.execute(
        select(AntivirusInstance).where(AntivirusInstance.id == instance_id)
    )
    instance = result.scalar_one_or_none()
    
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instance {instance_id} not found"
        )
    
    # Get log count
    log_count_result = await db.execute(
        select(func.count(LogEntry.id)).where(LogEntry.instance_id == instance.id)
    )
    log_count = log_count_result.scalar()
    
    instance_dict = instance.to_dict()
    instance_dict['log_count'] = log_count
    
    return AntivirusInstanceResponse(**instance_dict)


@router.patch(
    "/instances/{instance_id}",
    response_model=AntivirusInstanceResponse,
    summary="Update instance",
    description="Update instance metadata (status, hostname, etc.)"
)
async def update_instance(
    instance_id: str,
    update_data: AntivirusInstanceUpdate,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Update instance"""
    
    result = await db.execute(
        select(AntivirusInstance).where(AntivirusInstance.id == instance_id)
    )
    instance = result.scalar_one_or_none()
    
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instance {instance_id} not found"
        )
    
    # Update fields
    for key, value in update_data.dict(exclude_unset=True).items():
        if value is not None:
            if key == 'metadata' and isinstance(value, dict):
                import json
                setattr(instance, key, json.dumps(value))
            else:
                setattr(instance, key, value)
    
    instance.last_seen = datetime.utcnow()
    
    await db.commit()
    await db.refresh(instance)
    
    # Get log count
    log_count_result = await db.execute(
        select(func.count(LogEntry.id)).where(LogEntry.instance_id == instance.id)
    )
    log_count = log_count_result.scalar()
    
    instance_dict = instance.to_dict()
    instance_dict['log_count'] = log_count
    
    return AntivirusInstanceResponse(**instance_dict)


@router.delete(
    "/instances/{instance_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete instance",
    description="Delete an instance and all its logs (cascade)"
)
async def delete_instance(
    instance_id: str,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Delete instance and all its logs"""
    
    result = await db.execute(
        select(AntivirusInstance).where(AntivirusInstance.id == instance_id)
    )
    instance = result.scalar_one_or_none()
    
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instance {instance_id} not found"
        )
    
    await db.delete(instance)
    await db.commit()
    
    return None
