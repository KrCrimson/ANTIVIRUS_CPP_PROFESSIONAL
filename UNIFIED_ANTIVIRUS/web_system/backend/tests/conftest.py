"""
Test configuration and fixtures for Web Logging Server
=====================================================
"""

import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db
from app.models import Base
from app.config import settings


# Test database configuration
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db():
    """Create test database and clean it up after test"""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Yield session
    async with TestSessionLocal() as session:
        yield session
    
    # Clean up
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db():
    """Override database dependency for testing"""
    async with TestSessionLocal() as session:
        yield session


# Override dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def client():
    """Create test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_log_data():
    """Sample log data for testing"""
    return {
        "timestamp": "2024-11-07T15:30:00Z",
        "level": "INFO",
        "component": "core.engine",
        "message": "Test log message",
        "source_host": "test-host",
        "extra_data": {"test": "data"}
    }


@pytest.fixture
def auth_headers():
    """Authentication headers for testing"""
    return {"X-API-Key": "antivirus-system-key-2024"}