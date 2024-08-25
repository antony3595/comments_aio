from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.news import News
from schema.db.news import NewsSchema


class NewsRepository:
    async def read_all(self, db: AsyncSession, **kwargs) -> List[NewsSchema]:
        stmt = await db.execute(select(News))
        news = stmt.scalars().all()

        return [NewsSchema.model_validate(news_item, from_attributes=True) for news_item in news]
