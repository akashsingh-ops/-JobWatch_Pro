"""
Redis client configuration for caching and sessions
"""

import redis.asyncio as redis
from app.core.config import settings


# Create async Redis client
redis_client = redis.Redis.from_url(
    settings.redis_url,
    decode_responses=True,
    retry_on_timeout=True,
    socket_connect_timeout=5,
    socket_timeout=5,
)


async def get_cache(key: str) -> str | None:
    """
    Get value from cache
    """
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"Cache get error: {e}")
        return None


async def set_cache(key: str, value: str, expire: int = 300) -> bool:
    """
    Set value in cache with expiration
    """
    try:
        return await redis_client.setex(key, expire, value)
    except Exception as e:
        print(f"Cache set error: {e}")
        return False


async def delete_cache(key: str) -> int:
    """
    Delete value from cache
    """
    try:
        return await redis_client.delete(key)
    except Exception as e:
        print(f"Cache delete error: {e}")
        return 0


async def get_user_session(user_id: str) -> dict | None:
    """
    Get user session data
    """
    try:
        session_data = await redis_client.get(f"session:{user_id}")
        if session_data:
            import json
            return json.loads(session_data)
        return None
    except Exception as e:
        print(f"Session get error: {e}")
        return None


async def set_user_session(user_id: str, session_data: dict, expire: int = 3600) -> bool:
    """
    Set user session data
    """
    try:
        import json
        return await redis_client.setex(
            f"session:{user_id}",
            expire,
            json.dumps(session_data)
        )
    except Exception as e:
        print(f"Session set error: {e}")
        return False


async def clear_user_session(user_id: str) -> int:
    """
    Clear user session
    """
    try:
        return await redis_client.delete(f"session:{user_id}")
    except Exception as e:
        print(f"Session clear error: {e}")
        return 0
