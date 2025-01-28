from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from repository.raw_news import RawNewsRepository, get_raw_news_repository
from schema.db.raw_news import CreateRawNewsSchema, RawNewsSchema


class RawNewsService:
    @staticmethod
    async def create_raw_news(db: AsyncSession, service_account_id: int, raw_news_data: Dict[str, Any]) -> RawNewsSchema:
        data = CreateRawNewsSchema(service_account_id=service_account_id, data=raw_news_data)
        raw_news_repository = get_raw_news_repository()
        raw_news = await raw_news_repository.create(db, data)
        return raw_news
