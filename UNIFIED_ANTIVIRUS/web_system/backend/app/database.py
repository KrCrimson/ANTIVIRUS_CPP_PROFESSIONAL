"""
Database configuration and session management
============================================

Async SQLAlchemy setup with connection pooling
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from .config import settings
from .models import Base
import logging

logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    future=True,
    pool_pre_ping=True,
    # SQLite specific settings
    poolclass=StaticPool if "sqlite" in settings.database_url else None,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables created successfully")


async def drop_tables():
    """Drop all database tables (for testing)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("🗑️ Database tables dropped")


async def get_db():
    """
    Dependency to get database session
    
    Usage:
        @app.post("/api/logs")
        async def create_log(log_data: dict, db: AsyncSession = Depends(get_db)):
            # Use db session here
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_database():
    """Initialize database with tables and default data"""
    try:
        # Create tables
        await create_tables()
        
        # Create default API keys if needed
        await _create_default_api_keys()
        
        logger.info("🚀 Database initialization completed")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


async def _create_default_api_keys():
    """Create default API keys for development"""
    from .models import APIKey
    from .auth import hash_api_key
    
    async with AsyncSessionLocal() as session:
        try:
            # Check if any API keys exist
            from sqlalchemy import select
            result = await session.execute(select(APIKey))
            existing_keys = result.scalars().first()
            
            if not existing_keys:
                logger.info("Creating default API keys...")
                
                # Create default keys
                default_keys = [
                    {
                        "key": "antivirus-system-key-2024",
                        "name": "Antivirus System",
                        "description": "Default key for antivirus log submission",
                        "can_read": "true",
                        "can_write": "true"
                    },
                    {
                        "key": "dashboard-client-key-2024", 
                        "name": "Dashboard Client",
                        "description": "Default key for dashboard read access",
                        "can_read": "true",
                        "can_write": "false"
                    }
                ]
                
                for key_data in default_keys:
                    api_key = APIKey(
                        key_hash=hash_api_key(key_data["key"]),
                        name=key_data["name"],
                        description=key_data["description"],
                        can_read=key_data["can_read"],
                        can_write=key_data["can_write"]
                    )
                    session.add(api_key)
                
                await session.commit()
                logger.info(f"✅ Created {len(default_keys)} default API keys")
            else:
                logger.info("API keys already exist, skipping creation")
                
        except Exception as e:
            logger.error(f"❌ Failed to create default API keys: {e}")
            await session.rollback()


# Health check for database
async def check_database_health() -> bool:
    """Check if database is accessible"""
    try:
        async with AsyncSessionLocal() as session:
            # Simple query to test connection
            from sqlalchemy import text
            await session.execute(text("SELECT 1"))
            return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False