import asyncio
import logging

from pydantic import ValidationError

__all__ = ["process_raw_news"]

from db.connections.postgres_null_pool import get_null_pool_async_session

from schema.db.raw_news import UpdateRawNewsSchema
from services.news.news_service import NewsService
from services.raw_news.raw_news import RawNewsService
from tasks.celery import app

from tasks.push_notification import send_push_notification


@app.task(queue="ingest_queue")
def process_raw_news(raw_news_id: int) -> int:
    logging.info(f'processing raw news: id="{raw_news_id}"')
    res = asyncio.run(create_news_from_raw_news(raw_news_id))
    logging.info(f'raw news processed successfully: id="{raw_news_id}"')
    return res


async def create_news_from_raw_news(raw_news_id: int) -> int:
    async with get_null_pool_async_session() as db:
        raw_news_service = RawNewsService()
        news_service = NewsService()

        raw_news = await raw_news_service.get_by_id(db, raw_news_id)

        try:
            news = await news_service.create_from_raw_news(db, raw_news)
            categories = [c.category for c in news.categories]
            logging.info(
                f"raw news created successfully: news: {news.model_dump()}, categories={categories} raw={raw_news.model_dump()}"
            )

            subscribers = await news_service.get_subsribers_by_categories(
                db, categories=categories
            )

            for subscriber in subscribers:
                send_push_notification.delay(news.title, subscriber.id)
            return news.id
        except ValidationError as e:
            logging.info(
                f"raw news processed with errors: {e.errors()}, raw={raw_news.model_dump()}"
            )
        finally:
            await raw_news_service.update(
                db, raw_news_id, UpdateRawNewsSchema(processed=True)
            )
