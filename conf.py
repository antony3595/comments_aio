import logging
import os
import sys

from pydantic import SecretStr

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

BLOGS_API_URL = os.environ.get("BLOGS_API_URL", "https://jsonplaceholder.typicode.com")
CONSUMERS_COUNT = int(os.environ.get("CONSUMERS_COUNT", "10"))

TCP_SERVER_HOST = os.environ.get("TCP_SERVER_HOST", "0.0.0.0")
TCP_SERVER_PORT = os.environ.get("TCP_SERVER_PORT", "8888")

TOKEN_MAX_TTL: int = 30

API_KEY: SecretStr = os.environ.get("API_KEY", "123")
SECRET_KEY = os.environ.get("SECRET_KEY", "123")
