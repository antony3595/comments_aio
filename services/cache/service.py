from typing import Any

from redis.typing import KeyT

from clients.redis.client import get_redis_client


class CacheService:

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False

    async def set(self, key: KeyT, value: Any, **kwargs):
        async with get_redis_client() as redis:
            await redis.set(key, value, **kwargs)

    async def get(
        self,
        key: KeyT,
    ) -> Any:
        async with get_redis_client() as redis:
            return await redis.get(key)


def get_cache_service() -> CacheService:
    return CacheService()
