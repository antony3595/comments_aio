from typing import Dict, Any, List

from sqlalchemy.ext.asyncio import AsyncSession

from repository.raw_news import get_raw_news_repository
from schema.db.raw_news import CreateRawNewsSchema, RawNewsSchema


class RawNewsService:
    @staticmethod
    async def create_raw_news(db: AsyncSession, service_account_id: int,
                              raw_news_data: Dict[str, Any]) -> RawNewsSchema:
        async with db.begin():
            data = CreateRawNewsSchema(service_account_id=service_account_id, data=raw_news_data)
            raw_news_repository = get_raw_news_repository()
            raw_news = await raw_news_repository.create(db, data)
            await db.commit()
            return raw_news

    @staticmethod
    async def create_raw_news_bulk(db: AsyncSession, service_account_id: int,
                                   raw_news_data_values: List[Dict[str, Any]]) -> List[RawNewsSchema]:
        async with db.begin():
            data = [CreateRawNewsSchema(service_account_id=service_account_id, data=data_item) for data_item in raw_news_data_values]
            raw_news_repository = get_raw_news_repository()
            raw_news = await raw_news_repository.create_bulk(db, data)
            await db.commit()
            return raw_news
