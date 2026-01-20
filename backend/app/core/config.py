"""
Application configuration using Pydantic settings
"""

import secrets
from typing import List, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """
    Application settings with environment variable support
    """

    # Database Configuration (SQLite for development)
    database_url: str = "sqlite+aiosqlite:///./data_watch_nexus.db"

    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"

    # Elasticsearch Configuration
    elasticsearch_host: str = "http://localhost:9200"
    elasticsearch_index_jobs: str = "jobs"
    elasticsearch_index_records: str = "records"

    # JWT Configuration
    secret_key: str = secrets.token_urlsafe(32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Application Configuration
    debug: bool = True
    app_name: str = "Data Watch Nexus"
    app_version: str = "1.0.0"

    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # Email Configuration
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None

    # Celery Configuration
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @validator("secret_key", pre=True)
    def validate_secret_key(cls, v):
        """Ensure secret key is not the default"""
        if v == "your-secret-key-here-change-in-production":
            return secrets.token_urlsafe(32)
        return v

    @property
    def database_async_url(self) -> str:
        """Convert sync database URL to async"""
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")


# Create global settings instance
settings = Settings()
