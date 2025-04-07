import asyncio
import logging

__all__ = ["process_stuck_raw_news_task"]

from db.connections.postgres_null_pool import get_null_pool_async_session

from schema.db.base import PaginationSchema

from schema.db.raw_news import RawNewsFiltersSchema
from services.raw_news.raw_news import get_raw_news_service
from tasks import process_raw_news
from tasks.celery import app


@app.task(queue="ingest_queue")
def process_stuck_raw_news_task():
    logging.info(f"processing stuck raw news")
    res = asyncio.run(process_stuck_raw_news())
    logging.info(f"stuck raw news processed successfully")
    return res


async def process_stuck_raw_news() -> None:
    async with get_null_pool_async_session() as db:
        filters = RawNewsFiltersSchema(processed=False)

        pagination = PaginationSchema(page=1, size=10)
        raw_news = await get_raw_news_service().read_all(db, filters=filters, pagination=pagination)

        for raw_news_item in raw_news:
            process_raw_news.delay(raw_news_item.id)
