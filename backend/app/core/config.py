"""
Configuration management following 12-factor app principles
"""

import os
import secrets
from typing import List, Optional, Union
from pathlib import Path

from pydantic import BaseSettings, validator, Field
from pydantic.types import SecretStr


class Settings(BaseSettings):
    """
    Application settings with environment-based configuration
    """

    # Application Settings
    app_name: str = Field(default="Data Watch Nexus", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")

    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=4, env="WORKERS")

    # Database Configuration
    database_url: str = Field(..., env="DATABASE_URL")
    database_pool_size: int = Field(default=20, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=30, env="DATABASE_MAX_OVERFLOW")

    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    redis_cache_ttl: int = Field(default=3600, env="REDIS_CACHE_TTL")

    # Elasticsearch Configuration
    elasticsearch_host: str = Field(default="http://localhost:9200", env="ELASTICSEARCH_HOST")
    elasticsearch_index_jobs: str = Field(default="jobs", env="ELASTICSEARCH_INDEX_JOBS")
    elasticsearch_index_records: str = Field(default="records", env="ELASTICSEARCH_INDEX_RECORDS")
    elasticsearch_index_users: str = Field(default="users", env="ELASTICSEARCH_INDEX_USERS")

    # JWT Configuration
    secret_key: Union[str, SecretStr] = Field(default_factory=lambda: secrets.token_urlsafe(32), env="SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    # Email Configuration
    smtp_server: str = Field(default="smtp.gmail.com", env="SMTP_SERVER")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    smtp_password: Optional[SecretStr] = Field(default=None, env="SMTP_PASSWORD")
    email_from: str = Field(default="noreply@datawatchnexus.com", env="EMAIL_FROM")
    email_from_name: str = Field(default="Data Watch Nexus", env="EMAIL_FROM_NAME")

    # File Upload Configuration
    upload_path: str = Field(default="uploads/", env="UPLOAD_PATH")
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    allowed_extensions: List[str] = Field(default=["pdf", "doc", "docx", "txt"], env="ALLOWED_EXTENSIONS")

    # Celery Configuration
    celery_broker_url: str = Field(default="redis://localhost:6379/0", env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://localhost:6379/0", env="CELERY_RESULT_BACKEND")
    celery_timezone: str = Field(default="UTC", env="CELERY_TIMEZONE")

    # Security Configuration
    cors_origins: List[str] = Field(default=["http://localhost:3000", "http://localhost:8080"], env="CORS_ORIGINS")
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")

    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")

    # Monitoring & Analytics
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")

    # External APIs
    linkedin_api_key: Optional[SecretStr] = Field(default=None, env="LINKEDIN_API_KEY")
    github_api_key: Optional[SecretStr] = Field(default=None, env="GITHUB_API_KEY")

    # Feature Flags
    enable_recommendations: bool = Field(default=True, env="ENABLE_RECOMMENDATIONS")
    enable_notifications: bool = Field(default=True, env="ENABLE_NOTIFICATIONS")
    enable_email: bool = Field(default=True, env="ENABLE_EMAIL")
    enable_search_analytics: bool = Field(default=True, env="ENABLE_SEARCH_ANALYTICS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @validator("secret_key", pre=True)
    def validate_secret_key(cls, v):
        """Ensure secret key is not the default placeholder"""
        if v and v.startswith("your-"):
            return secrets.token_urlsafe(32)
        return v

    @validator("cors_origins", pre=True)
    def validate_cors_origins(cls, v):
        """Parse CORS origins from string if needed"""
        if isinstance(v, str):
            # Remove brackets and quotes, split by comma
            v = v.strip("[]").replace('"', '').replace("'", '').split(',')
            v = [origin.strip() for origin in v if origin.strip()]
        return v or ["http://localhost:3000"]

    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "production"

    @property
    def upload_directory(self) -> Path:
        """Get the absolute path for uploads"""
        return Path(self.upload_path).resolve()

    @property
    def database_async_url(self) -> str:
        """Convert sync database URL to async"""
        if self.database_url.startswith("postgresql://"):
            return self.database_url.replace("postgresql://", "postgresql+asyncpg://")
        elif self.database_url.startswith("sqlite:///"):
            return self.database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
        return self.database_url


# Create global settings instance
settings = Settings()