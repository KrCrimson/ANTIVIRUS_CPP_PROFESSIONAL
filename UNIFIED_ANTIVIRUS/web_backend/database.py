"""
Database models and initialization for PostgreSQL
"""
from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer, JSON, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class LogEntry(Base):
    """Modelo para almacenar logs"""
    __tablename__ = 'log_entries_v5'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=False), nullable=False)
    level = Column(String(20), nullable=False, index=True)
    component = Column(String(100), nullable=False, index=True)
    message = Column(Text, nullable=False)
    instance_id = Column(String(100), index=True)
    details = Column(JSON)
    received_at = Column(DateTime(timezone=False), server_default=func.now())

class AntivirusInstance(Base):
    """Modelo para almacenar instancias de antivirus"""
    __tablename__ = 'antivirus_instances_v5'
    
    id = Column(String(100), primary_key=True)
    hostname = Column(String(255))
    os_info = Column(String(255))
    antivirus_version = Column(String(50))
    status = Column(String(20), default='active', index=True)
    last_seen = Column(DateTime(timezone=False), server_default=func.now())
    created_at = Column(DateTime(timezone=False), server_default=func.now())

# Database connection
def get_database_url():
    """Get database URL from environment"""
    return os.getenv("DATABASE_URL", "")

def init_db():
    """Initialize database and create tables"""
    database_url = get_database_url()
    if not database_url:
        print("WARNING: No DATABASE_URL configured, using in-memory storage")
        return None, None
    
    # Create engine
    engine = create_engine(database_url, pool_pre_ping=True)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    return engine, SessionLocal

def get_db_session(SessionLocal):
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Don't close here, let the caller handle it
