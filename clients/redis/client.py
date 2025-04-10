import redis.asyncio as redis
from pydantic import SecretStr
from redis.asyncio import Redis

import config


class RedisClient:
    def __init__(self, connection_string: SecretStr) -> None:
        self.connection_string = connection_string

    async def __aenter__(self) -> Redis:
        self.client = self.get_client()
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def get_client(self) -> redis.Redis:
        return redis.from_url(self.connection_string.get_secret_value())


def get_redis_client() -> RedisClient:
    return RedisClient(config.settings.REDIS_URL)
