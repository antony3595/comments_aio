import logging
import os
import sys

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)

BLOGS_API_URL = os.environ.get("BLOGS_API_URL", "https://jsonplaceholder.typicode.com")

CONSUMERS_COUNT = int(os.environ.get("CONSUMERS_COUNT", "10"))
