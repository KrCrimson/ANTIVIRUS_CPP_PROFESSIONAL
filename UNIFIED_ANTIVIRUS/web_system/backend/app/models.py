"""
Database models for Web Logging Server
=====================================

SQLAlchemy models for storing antivirus logs
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
import json

Base = declarative_base()


class LogEntry(Base):
    """
    Main table for storing antivirus log entries
    
    Stores all logs received from the antivirus system with
    structured data and efficient querying capabilities.
    """
    __tablename__ = "log_entries"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Core log data
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    level = Column(String(20), nullable=False, index=True)  # INFO, WARNING, ERROR, etc.
    component = Column(String(100), nullable=False, index=True)  # core.engine, plugins.detector
    message = Column(Text, nullable=False)
    
    # Source information
    source_host = Column(String(100), nullable=True, index=True)  # Which antivirus instance
    source_process = Column(String(50), nullable=True)  # Process name/PID
    
    # Structured extra data as JSON
    extra_data = Column(Text, nullable=True)  # JSON string for flexible data
    
    # Performance metrics (if available)
    cpu_usage = Column(Float, nullable=True)
    memory_usage = Column(Float, nullable=True)
    
    # Threat-specific fields
    threat_type = Column(String(50), nullable=True, index=True)  # KEYLOGGER, MALWARE, etc.
    confidence_score = Column(Float, nullable=True)  # Detection confidence 0.0-1.0
    severity = Column(String(20), nullable=True, index=True)  # LOW, MEDIUM, HIGH, CRITICAL
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    received_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_timestamp_level', timestamp, level),
        Index('idx_component_timestamp', component, timestamp),
        Index('idx_threat_severity', threat_type, severity),
        Index('idx_received_at_desc', received_at.desc()),
    )
    
    def __repr__(self):
        return f"<LogEntry(id={self.id}, timestamp={self.timestamp}, level={self.level}, component={self.component})>"
    
    def to_dict(self) -> dict:
        """Convert log entry to dictionary for JSON serialization"""
        result = {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'level': self.level,
            'component': self.component,
            'message': self.message,
            'source_host': self.source_host,
            'source_process': self.source_process,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'threat_type': self.threat_type,
            'confidence_score': self.confidence_score,
            'severity': self.severity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'received_at': self.received_at.isoformat() if self.received_at else None,
        }
        
        # Parse extra_data JSON if present
        if self.extra_data:
            try:
                result['extra_data'] = json.loads(self.extra_data)
            except json.JSONDecodeError:
                result['extra_data'] = {'raw': self.extra_data}
        else:
            result['extra_data'] = {}
        
        return result


class LogStatistics(Base):
    """
    Pre-computed statistics for dashboard performance
    
    Stores aggregated statistics to avoid expensive queries
    on large log tables.
    """
    __tablename__ = "log_statistics"
    
    id = Column(Integer, primary_key=True)
    
    # Time period for statistics
    period_start = Column(DateTime(timezone=True), nullable=False, index=True)
    period_end = Column(DateTime(timezone=True), nullable=False, index=True)
    period_type = Column(String(20), nullable=False)  # 'hour', 'day', 'week', 'month'
    
    # Counts by level
    count_debug = Column(Integer, default=0)
    count_info = Column(Integer, default=0)
    count_warning = Column(Integer, default=0)
    count_error = Column(Integer, default=0)
    count_critical = Column(Integer, default=0)
    
    # Counts by component
    component_stats = Column(Text)  # JSON: {"core.engine": 123, "plugins.detector": 456}
    
    # Threat statistics
    threats_detected = Column(Integer, default=0)
    avg_confidence = Column(Float, nullable=True)
    critical_threats = Column(Integer, default=0)
    
    # Performance metrics
    avg_cpu_usage = Column(Float, nullable=True)
    avg_memory_usage = Column(Float, nullable=True)
    
    # Metadata
    computed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<LogStatistics(period={self.period_type}, start={self.period_start})>"


class APIKey(Base):
    """
    API Keys for authentication
    
    Stores API keys with metadata for access control
    """
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True)
    key_hash = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)  # Human-readable name
    description = Column(Text, nullable=True)
    
    # Permissions (simple role-based)
    can_read = Column(String(10), default="true")  # "true"/"false" as string
    can_write = Column(String(10), default="true")
    
    # Usage tracking
    last_used = Column(DateTime(timezone=True), nullable=True)
    usage_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(String(10), default="true")
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<APIKey(name={self.name}, active={self.is_active})>"