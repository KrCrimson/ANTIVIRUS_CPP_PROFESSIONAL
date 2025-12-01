"""
Database models for Web Logging Server
=====================================

SQLAlchemy models for storing antivirus logs with multi-instance support
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Index, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
import json
import uuid

Base = declarative_base()


class AntivirusInstance(Base):
    """
    Represents a unique antivirus installation/instance
    
    Each computer that downloads and installs the antivirus
    gets a unique instance ID for tracking and log association.
    """
    __tablename__ = "antivirus_instances"
    
    # Primary key - UUID for global uniqueness
    id = Column(String(36), primary_key=True, index=True)  # UUID format
    
    # Instance metadata
    hostname = Column(String(255), nullable=True)  # Computer hostname
    os_info = Column(String(200), nullable=True)  # OS type and version
    antivirus_version = Column(String(50), nullable=True)  # Antivirus version installed
    
    # Location/network info
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    mac_address = Column(String(17), nullable=True)  # MAC address
    
    # Status tracking
    status = Column(String(20), default="active", index=True)  # active, inactive, uninstalled
    last_seen = Column(DateTime(timezone=True), nullable=True, index=True)
    
    # Installation info
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    install_date = Column(DateTime(timezone=True), nullable=True)
    
    # Custom metadata as JSON
    metadata = Column(Text, nullable=True)  # JSON string for flexible data
    
    # Relationship to logs
    logs = relationship("LogEntry", back_populates="instance", cascade="all, delete-orphan")
    
    # Index for quick lookups
    __table_args__ = (
        Index('idx_status_lastseen', status, last_seen.desc()),
        Index('idx_hostname', hostname),
    )
    
    def __repr__(self):
        return f"<AntivirusInstance(id={self.id}, hostname={self.hostname}, status={self.status})>"
    
    def to_dict(self) -> dict:
        """Convert instance to dictionary for JSON serialization"""
        result = {
            'id': self.id,
            'hostname': self.hostname,
            'os_info': self.os_info,
            'antivirus_version': self.antivirus_version,
            'ip_address': self.ip_address,
            'mac_address': self.mac_address,
            'status': self.status,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'install_date': self.install_date.isoformat() if self.install_date else None,
        }
        
        # Parse metadata JSON if present
        if self.metadata:
            try:
                result['metadata'] = json.loads(self.metadata)
            except json.JSONDecodeError:
                result['metadata'] = {'raw': self.metadata}
        else:
            result['metadata'] = {}
        
        return result


class LogEntry(Base):
    """
    Main table for storing antivirus log entries
    
    Stores all logs received from the antivirus system with
    structured data and efficient querying capabilities.
    """
    __tablename__ = "log_entries"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to antivirus instance
    instance_id = Column(String(36), ForeignKey('antivirus_instances.id'), nullable=True, index=True)
    
    # Core log data
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    level = Column(String(20), nullable=False, index=True)  # INFO, WARNING, ERROR, etc.
    component = Column(String(100), nullable=False, index=True)  # core.engine, plugins.detector
    message = Column(Text, nullable=False)
    
    # Source information (legacy - now prefer instance_id)
    source_host = Column(String(100), nullable=True, index=True)  # Which antivirus instance
    source_process = Column(String(50), nullable=True)  # Process name/PID
    
    # Structured extra data as JSON
    extra_data = Column(Text, nullable=True)  # JSON string for flexible data
    
    # Relationship to instance
    instance = relationship("AntivirusInstance", back_populates="logs")
    
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
        Index('idx_instance_timestamp', instance_id, timestamp.desc()),
    )
    
    def __repr__(self):
        return f"<LogEntry(id={self.id}, timestamp={self.timestamp}, level={self.level}, component={self.component})>"
    
    def to_dict(self) -> dict:
        """Convert log entry to dictionary for JSON serialization"""
        result = {
            'id': self.id,
            'instance_id': self.instance_id,
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
        
        # Include instance info if available
        if self.instance:
            result['instance'] = {
                'id': self.instance.id,
                'hostname': self.instance.hostname,
                'status': self.instance.status
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