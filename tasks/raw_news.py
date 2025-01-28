import asyncio
import logging

from celery.app import Celery
from kombu import Queue
from pydantic import ValidationError

from config import settings

__all__ = ["process_raw_news"]

from db.connections.postgres import get_async_session
from repository.news import get_news_repository

from repository.raw_news import get_raw_news_repository
from schema.db.news import CreateNewsSchema

from schema.db.raw_news import UpdateRawNewsSchema

logger = logging.getLogger(__name__)

app = Celery(__name__, broker=settings.REDIS_URL.get_secret_value(), backend=settings.REDIS_URL.get_secret_value())

app.conf.task_queues = [
    Queue("ingest_queue")
]
app.conf.task_default_queue = 'ingest_queue'


@app.task
def process_raw_news(raw_news_id: int) -> None:
    logger.info(f"processing raw news: {raw_news_id}")
    asyncio.run(create_raw_news(raw_news_id))


async def create_raw_news(raw_news_id: int):
    async with get_async_session() as db:
        raw_news_repository = get_raw_news_repository()
        news_repository = get_news_repository()
        raw_news = await raw_news_repository.read(db, raw_news_id)

        try:
            news_values = CreateNewsSchema.model_validate(raw_news.data)
            news = await news_repository.create(db, news_values)
            logger.info(f"raw news created successfully: news: {news.model_dump()}, raw={raw_news.model_dump()}")
        except ValidationError as e:
            logger.info(f"raw news processed with errors: {e.errors()}, raw={raw_news.model_dump()}")
        finally:
            await raw_news_repository.update(db, raw_news_id, UpdateRawNewsSchema(processed=True))
