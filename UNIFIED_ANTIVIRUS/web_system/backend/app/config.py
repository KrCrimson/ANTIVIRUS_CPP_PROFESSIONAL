"""
Configuration settings for Web Logging Server
=============================================

Environment-based configuration using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    app_name: str = "Antivirus Web Logging Server"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    reload: bool = Field(default=False, env="RELOAD")
    
    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./logs.db",
        env="DATABASE_URL"
    )
    
    # PostgreSQL example: "postgresql+asyncpg://user:pass@localhost/logs_db"
    # SQLite example: "sqlite+aiosqlite:///./logs.db"
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    api_key_header: str = Field(default="X-API-Key", env="API_KEY_HEADER")
    
    # Default API keys (in production, use environment variables)
    default_api_keys: list[str] = Field(
        default=[
            "antivirus-system-key-2024",
            "dashboard-client-key-2024"
        ],
        env="DEFAULT_API_KEYS"
    )
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    max_log_entries: int = Field(default=100000, env="MAX_LOG_ENTRIES")
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=1000, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")  # seconds
    
    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        env="CORS_ORIGINS"
    )
    
    # Pagination
    default_page_size: int = Field(default=50, env="DEFAULT_PAGE_SIZE")
    max_page_size: int = Field(default=500, env="MAX_PAGE_SIZE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()