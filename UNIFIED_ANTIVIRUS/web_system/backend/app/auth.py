"""
Authentication and authorization system
======================================

API Key-based authentication for the logging server
"""

import hashlib
import hmac
from typing import Optional
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import APIKey
from .database import get_db
from .config import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer(auto_error=False)


def hash_api_key(api_key: str) -> str:
    """Create a secure hash of the API key"""
    return hashlib.sha256(
        (api_key + settings.secret_key).encode()
    ).hexdigest()


def verify_api_key(api_key: str, key_hash: str) -> bool:
    """Verify an API key against its hash"""
    return hmac.compare_digest(
        hash_api_key(api_key),
        key_hash
    )


async def get_api_key_from_header(request: Request) -> Optional[str]:
    """Extract API key from custom header or Authorization header"""
    
    # Try custom header first (X-API-Key)
    api_key = request.headers.get(settings.api_key_header)
    if api_key:
        return api_key
    
    # Try Authorization header (Bearer token)
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.replace("Bearer ", "")
    
    return None


async def get_current_api_key(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> APIKey:
    """
    Dependency to get and validate current API key
    
    Raises HTTPException if invalid or missing
    """
    
    # Extract API key from request
    api_key = await get_api_key_from_header(request)
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Provide via X-API-Key header or Authorization: Bearer <key>",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validate against database
    try:
        stmt = select(APIKey).where(APIKey.is_active == "true")
        result = await db.execute(stmt)
        api_keys = result.scalars().all()
        
        for stored_key in api_keys:
            if verify_api_key(api_key, stored_key.key_hash):
                # Update last used timestamp and usage count
                stored_key.last_used = datetime.utcnow()
                stored_key.usage_count += 1
                await db.commit()
                
                logger.info(f"✅ API key authenticated: {stored_key.name}")
                return stored_key
        
        # Also check default keys from settings for development
        if api_key in settings.default_api_keys:
            logger.info(f"✅ Default API key authenticated: {api_key}")
            # Return a mock APIKey for default keys
            return APIKey(
                name="Default Key",
                description="Development default key",
                can_read="true",
                can_write="true",
                is_active="true"
            )
        
        # No valid key found
        logger.warning(f"❌ Invalid API key attempted: {api_key[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ API key validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error"
        )


async def require_write_permission(api_key: APIKey = Depends(get_current_api_key)) -> APIKey:
    """
    Dependency that requires write permissions
    
    Use this for endpoints that modify data (POST, PUT, DELETE)
    """
    if api_key.can_write != "true":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Write permission required"
        )
    return api_key


async def require_read_permission(api_key: APIKey = Depends(get_current_api_key)) -> APIKey:
    """
    Dependency that requires read permissions
    
    Use this for endpoints that read data (GET)
    """
    if api_key.can_read != "true":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Read permission required"
        )
    return api_key


# Rate limiting (simple in-memory implementation)
from collections import defaultdict
import time

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, max_requests: int = 1000, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed for the given key"""
        now = time.time()
        
        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if now - req_time < self.window_seconds
        ]
        
        # Check limit
        if len(self.requests[key]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter(
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window
)


async def check_rate_limit(
    request: Request,
    api_key: APIKey = Depends(get_current_api_key)
):
    """
    Rate limiting dependency
    
    Limits requests per API key
    """
    client_id = f"{api_key.name}:{request.client.host if request.client else 'unknown'}"
    
    if not rate_limiter.is_allowed(client_id):
        logger.warning(f"⚠️ Rate limit exceeded for {client_id}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {settings.rate_limit_requests} requests per {settings.rate_limit_window} seconds"
        )
    
    return api_key