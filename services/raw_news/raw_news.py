from typing import Dict, Any

from db.connections.postgres import async_session
from repository.raw_news import get_raw_news_repository
from schema.db.raw_news import CreateRawNewsSchema, RawNewsSchema


class RawNewsService:
    @staticmethod
    async def create_raw_news(service_account_id: int,
                              raw_news_data: Dict[str, Any]) -> RawNewsSchema:
        async with async_session() as db:
            async with db.begin():
                data = CreateRawNewsSchema(service_account_id=service_account_id, data=raw_news_data)
                raw_news_repository = get_raw_news_repository()
                raw_news = await raw_news_repository.create(db, data)
                await db.commit()
                return raw_news
