"""
Twitter Scraping Bot - Main Entry Point
"""

import uvicorn

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Start the FastAPI application."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"API will be available at http://{settings.api_host}:{settings.api_port}")
    logger.info(f"API Documentation at http://{settings.api_host}:{settings.api_port}/docs")
    
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
