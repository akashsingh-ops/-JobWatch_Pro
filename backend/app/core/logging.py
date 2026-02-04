"""
Structured logging configuration
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False

from app.core.config import settings


def setup_logging():
    """
    Setup structured logging with appropriate formatters and handlers
    """
    if not STRUCTLOG_AVAILABLE:
        # Fallback to standard logging
        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper()),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler("logs/app.log", mode='a') if settings.is_production else logging.NullHandler()
            ]
        )
        return

    # Configure structlog
    shared_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.log_format == "json":
        # JSON logging for production
        shared_processors.append(structlog.processors.JSONRenderer())
    else:
        # Human-readable logging for development
        shared_processors.append(
            structlog.dev.ConsoleRenderer(colors=True)
        )

    structlog.configure(
        processors=shared_processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )

    # Create logs directory if it doesn't exist
    if settings.is_production:
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        # Add file handler for production
        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setLevel(getattr(logging, settings.log_level.upper()))

        if settings.log_format == "json":
            # JSON formatter for file logs
            try:
                import json_log_formatter
                file_handler.setFormatter(json_log_formatter.JSONFormatter())
            except ImportError:
                pass  # Fallback to basic formatting
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)

        logging.getLogger().addHandler(file_handler)

    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("elasticsearch").setLevel(logging.WARNING)

    # Configure specific loggers
    if settings.sentry_dsn:
        try:
            import sentry_sdk
            sentry_sdk.init(
                dsn=settings.sentry_dsn,
                environment=settings.environment,
                release=settings.app_version,
            )
            logger.info("Sentry error monitoring enabled")
        except ImportError:
            logger.warning("Sentry SDK not installed")


def get_logger(name: str) -> Any:
    """
    Get a configured logger instance
    """
    if STRUCTLOG_AVAILABLE:
        return structlog.get_logger(name)
    else:
        return logging.getLogger(name)


# Global logger instance
logger = get_logger(__name__)
