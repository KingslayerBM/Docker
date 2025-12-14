from __future__ import annotations

import os
from typing import Optional, Any


def create_redis_client() -> Optional[Any]:
    """Create Redis client if REDIS_HOST is set and redis library is installed.

    Returns None when Redis is not configured or not available.
    """
    host = os.getenv("REDIS_HOST")
    if not host:
        return None

    try:
        import redis  # type: ignore
    except Exception:
        return None

    port = int(os.getenv("REDIS_PORT", "6379"))
    db = int(os.getenv("REDIS_DB", "0"))
    return redis.Redis(
        host=host,
        port=port,
        db=db,
        socket_timeout=1.0,
        socket_connect_timeout=1.0,
    )
