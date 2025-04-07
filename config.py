import logging
import sys
from pprint import pprint

from pydantic import SecretStr
from pydantic_settings import BaseSettings

__all__ = ["settings"]

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)


class Settings(BaseSettings):
    DEBUG: bool = True
    BLOGS_API_URL: str = "https://jsonplaceholder.typicode.com"
    CONSUMERS_COUNT: int = 10
    TCP_SERVER_HOST: str = "0.0.0.0"
    TCP_SERVER_PORT: str = "8888"
    TOKEN_MAX_TTL: int = 3600
    API_KEY: SecretStr = "123"
    SECRET_KEY: SecretStr = "123"
    DB_CONNECTION_STRING: SecretStr = "postgresql+asyncpg://user:password@localhost:5435/comments_aio_db"
    REDIS_URL: SecretStr = "redis://localhost:6379"
    TIMEZONE: str = "Asia/Bishkek"


settings = Settings()
pprint(settings.dict())
