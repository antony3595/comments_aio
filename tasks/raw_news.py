import asyncio
import logging

from pydantic import ValidationError

__all__ = ["process_raw_news"]

from db.connections.postgres_null_pool import get_null_pool_async_session
from repository.news import get_news_repository
from repository.news_category import get_news_category_repository

from repository.raw_news import get_raw_news_repository
from schema.db.news import CreateNewsSchema
from schema.db.news_category import CreateNewsCategoriesSchema

from schema.db.raw_news import UpdateRawNewsSchema
from tasks.celery import app

from tasks.push_notification import send_push_notification


@app.task(queue='ingest_queue')
def process_raw_news(raw_news_id: int) -> int:
    logging.info(f"processing raw news: id=\"{raw_news_id}\"")
    res = asyncio.run(create_news_from_raw_news(raw_news_id))
    logging.info(f"raw news processed successfully: id=\"{raw_news_id}\"")
    return res


async def create_news_from_raw_news(raw_news_id: int) -> int:
    async with get_null_pool_async_session() as db:
        raw_news_repository = get_raw_news_repository()
        news_repository = get_news_repository()
        news_category_repository = get_news_category_repository()
        raw_news = await raw_news_repository.read(db, raw_news_id)
        categories = raw_news.data.pop('categories')

        try:
            news_values = CreateNewsSchema.model_validate(raw_news.data)
            news = await news_repository.create(db, news_values)

            news_categories_values = CreateNewsCategoriesSchema(news_id=news.id, categories=categories)
            news_categories = await news_category_repository.create(db, news_categories_values)
            logging.info(f"raw news created successfully: news: {news.model_dump()}, categories={categories} raw={raw_news.model_dump()}")

            subscribers = await news_category_repository.get_subscribed_users(db, categories=categories)

            for subscriber in subscribers:
                send_push_notification.delay(news.title, subscriber.id)
            return news.id
        except ValidationError as e:
            logging.info(f"raw news processed with errors: {e.errors()}, raw={raw_news.model_dump()}")
        finally:
            await raw_news_repository.update(db, raw_news_id, UpdateRawNewsSchema(processed=True))
