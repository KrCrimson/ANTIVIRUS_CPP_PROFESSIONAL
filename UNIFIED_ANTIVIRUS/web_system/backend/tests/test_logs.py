"""
Tests for log API endpoints
==========================
"""

import pytest
from httpx import AsyncClient


class TestLogAPI:
    """Test log-related API endpoints"""

    async def test_create_log_entry(self, client: AsyncClient, sample_log_data, auth_headers):
        """Test creating a single log entry"""
        response = await client.post(
            "/api/logs",
            json=sample_log_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["level"] == "INFO"
        assert data["component"] == "core.engine"
        assert data["message"] == "Test log message"
        assert data["id"] is not None

    async def test_create_log_without_auth(self, client: AsyncClient, sample_log_data):
        """Test creating log without authentication should fail"""
        response = await client.post("/api/logs", json=sample_log_data)
        
        assert response.status_code == 401

    async def test_create_log_invalid_data(self, client: AsyncClient, auth_headers):
        """Test creating log with invalid data should fail"""
        invalid_data = {
            "level": "INVALID_LEVEL",
            "message": ""  # Empty message
        }
        
        response = await client.post(
            "/api/logs",
            json=invalid_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422

    async def test_query_logs(self, client: AsyncClient, auth_headers):
        """Test querying logs with pagination"""
        response = await client.get(
            "/api/logs?page=1&size=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "logs" in data
        assert "total" in data
        assert "page" in data
        assert "pages" in data

    async def test_query_logs_with_filters(self, client: AsyncClient, auth_headers):
        """Test querying logs with filters"""
        response = await client.get(
            "/api/logs?level=INFO&component=core.engine",
            headers=auth_headers
        )
        
        assert response.status_code == 200

    async def test_get_log_by_id_not_found(self, client: AsyncClient, auth_headers):
        """Test getting non-existent log should return 404"""
        response = await client.get("/api/logs/99999", headers=auth_headers)
        
        assert response.status_code == 404