import json
from typing import Optional

import redis.asyncio as aioredis

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

_redis: Optional[aioredis.Redis] = None


async def init_redis() -> None:
    global _redis
    try:
        _redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        await _redis.ping()
        logger.info("redis_connected")
    except Exception as e:
        logger.warning("redis_unavailable", error=str(e))
        _redis = None


async def close_redis() -> None:
    global _redis
    if _redis:
        await _redis.aclose()
        _redis = None


class CacheService:
    """Кэш цен в Redis. При недоступности Redis — работает без кэша."""

    _PREFIX = "price:"
    _TTL    = settings.PRICE_CACHE_TTL

    @staticmethod
    def _available() -> bool:
        return _redis is not None

    @staticmethod
    async def get_prices() -> Optional[dict[str, int]]:
        if not CacheService._available():
            return None
        try:
            raw = await _redis.get("prices:all")
            return json.loads(raw) if raw else None
        except Exception:
            return None

    @staticmethod
    async def set_prices(prices: dict[str, int]) -> None:
        if not CacheService._available():
            return
        try:
            await _redis.setex("prices:all", CacheService._TTL, json.dumps(prices))
        except Exception:
            pass

    @staticmethod
    async def invalidate_prices() -> None:
        if not CacheService._available():
            return
        try:
            await _redis.delete("prices:all")
        except Exception:
            pass
