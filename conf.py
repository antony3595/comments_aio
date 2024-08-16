import logging
import os
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
    BLOGS_API_URL: str = "https://jsonplaceholder.typicode.com"
    CONSUMERS_COUNT: int = 10
    TCP_SERVER_HOST: str = "0.0.0.0"
    TCP_SERVER_PORT: str = "8888"
    TOKEN_MAX_TTL: int = 30
    API_KEY: SecretStr = os.environ.get("API_KEY", "123")
    SECRET_KEY: SecretStr = os.environ.get("SECRET_KEY", "123")


settings = Settings()
pprint(settings.dict())
