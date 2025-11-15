"""
Web Logging Server - FastAPI Application
=======================================

Main FastAPI application for receiving and serving antivirus logs
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import time
import json
from datetime import datetime

from .config import settings
from .database import init_database, check_database_health
from .routes import logs, stats, health
from .schemas import ErrorResponse

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    
    # Startup
    logger.info(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"🔧 Debug mode: {settings.debug}")
    logger.info(f"🏠 Host: {settings.host}:{settings.port}")
    
    try:
        # Initialize database
        await init_database()
        
        # Check database health
        if await check_database_health():
            logger.info("✅ Database connection verified")
        else:
            logger.error("❌ Database health check failed")
            
        logger.info("🎉 Application startup completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Application startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application...")
    logger.info("👋 Application shutdown completed")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="REST API server for collecting and serving antivirus logs in real-time",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)


# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Trust proxy headers (for deployment behind reverse proxy)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else [settings.host, "localhost", "127.0.0.1"]
)


# Request middleware for logging and timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing"""
    
    start_time = time.time()
    
    # Generate request ID for tracing
    request_id = f"{int(time.time())}-{id(request)}"
    
    # Log request
    logger.info(
        f"📨 {request.method} {request.url.path} - "
        f"Client: {request.client.host if request.client else 'unknown'} - "
        f"ID: {request_id}"
    )
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Add headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log response
    logger.info(
        f"📤 {response.status_code} - "
        f"Time: {process_time:.3f}s - "
        f"ID: {request_id}"
    )
    
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed messages"""
    
    error_details = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_details.append(f"{field}: {message}")
    
    logger.warning(f"❌ Validation error: {error_details}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="Validation Error",
            detail="; ".join(error_details),
            timestamp=datetime.utcnow(),
            request_id=request.headers.get("X-Request-ID")
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    
    logger.error(f"❌ Unexpected error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal Server Error",
            detail="An unexpected error occurred" if not settings.debug else str(exc),
            timestamp=datetime.utcnow(),
            request_id=request.headers.get("X-Request-ID")
        ).dict()
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "docs_url": "/docs" if settings.debug else "Documentation disabled in production",
        "endpoints": {
            "logs": "/api/logs",
            "statistics": "/api/stats", 
            "health": "/api/health"
        }
    }


# Include routers
app.include_router(
    logs.router,
    prefix="/api",
    tags=["Logs"]
)

app.include_router(
    stats.router,
    prefix="/api",
    tags=["Statistics"]
)

app.include_router(
    health.router,
    prefix="/api",
    tags=["Health"]
)


# Utility endpoints for monitoring
@app.get("/metrics")
async def metrics():
    """Basic metrics endpoint (Prometheus-compatible format would go here)"""
    
    # This could be expanded to return Prometheus metrics
    # For now, return basic JSON metrics
    
    return {
        "http_requests_total": "counter",
        "http_request_duration_seconds": "histogram", 
        "database_connections_active": "gauge",
        "logs_received_total": "counter",
        "errors_total": "counter"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )