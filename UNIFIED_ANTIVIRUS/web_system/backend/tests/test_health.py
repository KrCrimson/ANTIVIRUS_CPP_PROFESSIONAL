"""
Tests for health check endpoints
==============================
"""

import pytest
from httpx import AsyncClient


class TestHealthAPI:
    """Test health check endpoints"""

    async def test_health_check(self, client: AsyncClient):
        """Test basic health check endpoint"""
        response = await client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert "database_status" in data

    async def test_readiness_probe(self, client: AsyncClient):
        """Test Kubernetes readiness probe"""
        response = await client.get("/api/health/readiness")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "ready"

    async def test_liveness_probe(self, client: AsyncClient):
        """Test Kubernetes liveness probe"""
        response = await client.get("/api/health/liveness")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "alive"
        assert "uptime_seconds" in data

    async def test_startup_probe(self, client: AsyncClient):
        """Test Kubernetes startup probe"""
        response = await client.get("/api/health/startup")
        
        # Might be 200 or 503 depending on timing
        assert response.status_code in [200, 503]

    async def test_detailed_health_check(self, client: AsyncClient):
        """Test detailed health check endpoint"""
        response = await client.get("/api/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "basic_health" in data
        assert "system_metrics" in data
        assert "configuration" in data