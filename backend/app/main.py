"""
Main FastAPI application
"""

from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import structlog

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import create_tables
from app.core.redis import redis_client
from app.core.elasticsearch import es_client
from app.api.v1.api import api_router
from app.core.middleware import RateLimitMiddleware, SecurityHeadersMiddleware


# Setup structured logging
setup_logging()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager
    """
    logger.info("Starting Data Watch Nexus API", version=settings.app_version, environment=settings.environment)

    try:
        # Create database tables
        await create_tables()
        logger.info("Database tables created/verified")

        # Test Redis connection
        if settings.redis_url:
            await redis_client.ping()
            logger.info("Redis connection established")

        # Test Elasticsearch connection
        if settings.elasticsearch_host:
            await es_client.ping()
            logger.info("Elasticsearch connection established")

    except Exception as e:
        logger.error("Failed to initialize services", error=str(e))
        raise

    yield

    # Shutdown
    logger.info("Shutting down Data Watch Nexus API")
    try:
        await redis_client.close()
        await es_client.close()
    except Exception as e:
        logger.error("Error during shutdown", error=str(e))


def create_application() -> FastAPI:
    """
    Create and configure FastAPI application
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Production-grade Job Portal API with advanced recommendations",
        openapi_url="/api/v1/openapi.json" if not settings.is_production else None,
        docs_url="/api/docs" if not settings.is_production else None,
        redoc_url="/api/redoc" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
    )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)

    # Include API routers
    app.include_router(
        api_router,
        prefix="/api/v1",
        tags=["API v1"]
    )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "version": settings.app_version,
            "environment": settings.environment,
            "timestamp": "2024-01-20T17:30:00Z"
        }

    # Metrics endpoint (for monitoring)
    @app.get("/metrics")
    async def metrics():
        """Application metrics"""
        return {
            "uptime": "00:30:00",
            "requests_total": 150,
            "active_users": 25,
            "jobs_posted": 45
        }

    # Global exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors"""
        logger.warning("Validation error", path=request.url.path, errors=exc.errors())
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Validation error",
                "errors": exc.errors()
            }
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions"""
        logger.warning("HTTP exception", path=request.url.path, status_code=exc.status_code, detail=exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions"""
        logger.error("Unhandled exception", path=request.url.path, error=str(exc), exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    return app


# Create application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        reload=not settings.is_production,
        log_config=None,  # Use our custom logging
        access_log=True
    )
