#!/usr/bin/env python3
"""
Web Logging Server Startup Script
=================================

Production-ready startup script for the web logging server
"""

import uvicorn
import sys
import os
import logging
from pathlib import Path

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings


def main():
    """Main entry point"""
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    logger = logging.getLogger(__name__)
    
    logger.info(f"🚀 Starting {settings.app_name}")
    logger.info(f"🔧 Configuration:")
    logger.info(f"   - Host: {settings.host}")
    logger.info(f"   - Port: {settings.port}")
    logger.info(f"   - Debug: {settings.debug}")
    logger.info(f"   - Database: {settings.database_url}")
    logger.info(f"   - Log Level: {settings.log_level}")
    
    # Run server
    try:
        uvicorn.run(
            "app.main:app",
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
            log_level=settings.log_level.lower(),
            access_log=True,
            server_header=False,  # Security: don't expose server info
            date_header=False     # Security: don't expose date
        )
    except KeyboardInterrupt:
        logger.info("👋 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()