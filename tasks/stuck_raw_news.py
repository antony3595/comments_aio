import asyncio
import logging
from typing import List

__all__ = ["process_stuck_raw_news_task"]

from db.connections.postgres_null_pool import get_null_pool_async_session

from repository.raw_news import get_raw_news_repository
from schema.db.base import PaginationSchema

from schema.db.raw_news import RawNewsFiltersSchema
from tasks import process_raw_news
from tasks.celery import app


@app.task(queue="ingest_queue")
def process_stuck_raw_news_task():
    logging.info(f"processing stuck raw news")
    res = asyncio.run(process_stuck_raw_news())
    logging.info(f"stuck raw news processed successfully")
    return res


async def process_stuck_raw_news() -> List[int]:
    async with get_null_pool_async_session() as db:
        raw_news_repository = get_raw_news_repository()

        filters = RawNewsFiltersSchema(processed=False)

        pagination = PaginationSchema(page=1, size=10)
        raw_news = await raw_news_repository.read_all(db, filters=filters, pagination=pagination)

        for raw_news_item in raw_news:
            result = process_raw_news.delay(raw_news_item.id)

        return [i.id for i in raw_news]
