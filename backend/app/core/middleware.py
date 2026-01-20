"""
Custom middleware for security, rate limiting, and monitoring
"""

import time
import hashlib
import secrets
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

from app.core.config import settings
from app.core.redis import redis_client


logger = structlog.get_logger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "object-src 'none'; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using Redis
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/metrics"]:
            return await call_next(request)

        # Create rate limit key
        client_ip = self._get_client_ip(request)
        endpoint = request.url.path
        rate_limit_key = f"ratelimit:{client_ip}:{endpoint}"

        # Check current requests in window
        current_count = await redis_client.get(rate_limit_key)
        current_count = int(current_count) if current_count else 0

        if current_count >= settings.rate_limit_requests:
            logger.warning("Rate limit exceeded", client_ip=client_ip, endpoint=endpoint)
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests",
                    "retry_after": settings.rate_limit_window
                }
            )

        # Increment counter
        await redis_client.setex(rate_limit_key, settings.rate_limit_window, current_count + 1)

        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_requests)
        response.headers["X-RateLimit-Remaining"] = str(max(0, settings.rate_limit_requests - current_count - 1))
        response.headers["X-RateLimit-Reset"] = str(settings.rate_limit_window)

        return response

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for forwarded headers
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to client host
        return request.client.host if request.client else "unknown"


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Request logging middleware
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Create request ID
        request_id = secrets.token_hex(8)
        request.state.request_id = request_id

        # Log request
        logger.info(
            "Request started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params),
            client_ip=self._get_client_ip(request),
            user_agent=request.headers.get("User-Agent", "")
        )

        try:
            response = await call_next(request)

            # Log response
            process_time = time.time() - start_time
            logger.info(
                "Request completed",
                request_id=request_id,
                status_code=response.status_code,
                process_time=round(process_time * 1000, 2)  # ms
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            # Log error
            process_time = time.time() - start_time
            logger.error(
                "Request failed",
                request_id=request_id,
                error=str(e),
                process_time=round(process_time * 1000, 2),
                exc_info=True
            )
            raise


class APIVersioningMiddleware(BaseHTTPMiddleware):
    """
    API versioning middleware
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check for API versioning in headers
        api_version = request.headers.get("X-API-Version", "v1")

        # Add version to request state
        request.state.api_version = api_version

        # Check if version is supported
        supported_versions = ["v1"]
        if api_version not in supported_versions:
            return JSONResponse(
                status_code=400,
                content={
                    "detail": f"API version '{api_version}' is not supported",
                    "supported_versions": supported_versions
                }
            )

        response = await call_next(request)

        # Add version header to response
        response.headers["X-API-Version"] = api_version

        return response


class CacheMiddleware(BaseHTTPMiddleware):
    """
    Response caching middleware
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)

        # Create cache key
        cache_key = self._create_cache_key(request)

        # Check cache
        cached_response = await redis_client.get(cache_key)
        if cached_response:
            logger.info("Cache hit", cache_key=cache_key)
            # Parse cached response (would need proper serialization in production)
            return Response(content=cached_response, media_type="application/json")

        # Get response
        response = await call_next(request)

        # Cache successful GET responses
        if response.status_code == 200 and request.method == "GET":
            try:
                content = response.body.decode('utf-8')
                await redis_client.setex(cache_key, settings.redis_cache_ttl, content)
                logger.info("Response cached", cache_key=cache_key)
            except Exception as e:
                logger.warning("Failed to cache response", error=str(e))

        return response

    def _create_cache_key(self, request: Request) -> str:
        """Create cache key from request"""
        key_parts = [
            request.method,
            str(request.url),
            str(sorted(request.query_params.items()))
        ]

        # Add user ID if authenticated (would need to get from token)
        user_id = getattr(request.state, 'user_id', None)
        if user_id:
            key_parts.append(f"user:{user_id}")

        key_string = "|".join(key_parts)
        return f"cache:{hashlib.md5(key_string.encode()).hexdigest()}"
