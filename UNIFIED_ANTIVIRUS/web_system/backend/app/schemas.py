"""
Pydantic schemas for request/response validation
==============================================

Data validation and serialization schemas for the API
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class LogLevel(str, Enum):
    """Valid log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ThreatSeverity(str, Enum):
    """Valid threat severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class LogEntryCreate(BaseModel):
    """Schema for creating a new log entry"""
    
    # Required fields
    timestamp: datetime = Field(..., description="When the log was generated")
    level: LogLevel = Field(..., description="Log severity level")
    component: str = Field(..., min_length=1, max_length=100, description="Antivirus component name")
    message: str = Field(..., min_length=1, description="Log message content")
    
    # Optional source information
    source_host: Optional[str] = Field(None, max_length=100, description="Source hostname")
    source_process: Optional[str] = Field(None, max_length=50, description="Source process name")
    
    # Optional structured data
    extra_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional structured data")
    
    # Optional performance metrics
    cpu_usage: Optional[float] = Field(None, ge=0.0, le=100.0, description="CPU usage percentage")
    memory_usage: Optional[float] = Field(None, ge=0.0, description="Memory usage in MB")
    
    # Optional threat information
    threat_type: Optional[str] = Field(None, max_length=50, description="Type of threat detected")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Detection confidence")
    severity: Optional[ThreatSeverity] = Field(None, description="Threat severity level")
    
    @validator('message')
    def validate_message(cls, v):
        """Ensure message is not empty after stripping"""
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
    
    @validator('component')
    def validate_component(cls, v):
        """Normalize component name"""
        return v.strip().lower()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LogEntryResponse(BaseModel):
    """Schema for log entry responses"""
    
    id: int
    timestamp: datetime
    level: str
    component: str
    message: str
    source_host: Optional[str] = None
    source_process: Optional[str] = None
    extra_data: Dict[str, Any] = {}
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    threat_type: Optional[str] = None
    confidence_score: Optional[float] = None
    severity: Optional[str] = None
    created_at: datetime
    received_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LogQueryParams(BaseModel):
    """Schema for log query parameters"""
    
    # Pagination
    page: int = Field(default=1, ge=1, description="Page number (1-based)")
    size: int = Field(default=50, ge=1, le=500, description="Page size")
    
    # Filtering
    level: Optional[LogLevel] = Field(None, description="Filter by log level")
    component: Optional[str] = Field(None, description="Filter by component")
    source_host: Optional[str] = Field(None, description="Filter by source host")
    threat_type: Optional[str] = Field(None, description="Filter by threat type")
    severity: Optional[ThreatSeverity] = Field(None, description="Filter by severity")
    
    # Date range filtering
    date_from: Optional[datetime] = Field(None, description="Start date for filtering")
    date_to: Optional[datetime] = Field(None, description="End date for filtering")
    
    # Text search
    search: Optional[str] = Field(None, min_length=1, description="Search in message content")
    
    # Sorting
    sort_by: str = Field(default="received_at", description="Sort field")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$", description="Sort order")
    
    @validator('date_to')
    def validate_date_range(cls, v, values):
        """Ensure date_to is after date_from"""
        if v and 'date_from' in values and values['date_from']:
            if v <= values['date_from']:
                raise ValueError('date_to must be after date_from')
        return v


class LogQueryResponse(BaseModel):
    """Schema for paginated log query responses"""
    
    logs: List[LogEntryResponse]
    total: int = Field(..., description="Total number of logs matching query")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size used")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")


class LogStatisticsResponse(BaseModel):
    """Schema for log statistics"""
    
    total_logs: int
    logs_by_level: Dict[str, int]
    logs_by_component: Dict[str, int] 
    logs_by_hour: List[Dict[str, Any]]  # Time series data
    threats_detected: int
    avg_confidence: Optional[float] = None
    critical_threats: int
    top_components: List[Dict[str, Any]]
    date_range: Dict[str, datetime]


class HealthCheckResponse(BaseModel):
    """Schema for health check responses"""
    
    status: str = Field(..., description="Overall status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="API version")
    uptime_seconds: Optional[int] = Field(None, description="Server uptime")
    database_status: str = Field(..., description="Database connection status")
    total_logs: int = Field(..., description="Total logs in database")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(None, description="Request identifier for tracking")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class BulkLogCreate(BaseModel):
    """Schema for bulk log creation"""
    
    logs: List[LogEntryCreate] = Field(..., min_items=1, max_items=1000, description="List of logs to create")
    
    @validator('logs')
    def validate_logs_not_empty(cls, v):
        if not v:
            raise ValueError('At least one log entry required')
        return v


class BulkLogResponse(BaseModel):
    """Schema for bulk log creation responses"""
    
    created_count: int = Field(..., description="Number of logs successfully created")
    failed_count: int = Field(..., description="Number of logs that failed")
    errors: List[str] = Field(default_factory=list, description="Error messages for failed logs")
    created_ids: List[int] = Field(default_factory=list, description="IDs of created logs")


# API Key management schemas (for future admin endpoints)
class APIKeyCreate(BaseModel):
    """Schema for creating API keys"""
    
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    can_read: bool = True
    can_write: bool = True
    expires_at: Optional[datetime] = None


class APIKeyResponse(BaseModel):
    """Schema for API key responses (without the actual key)"""
    
    id: int
    name: str
    description: Optional[str] = None
    can_read: bool
    can_write: bool
    is_active: bool
    created_at: datetime
    last_used: Optional[datetime] = None
    usage_count: int
    expires_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True