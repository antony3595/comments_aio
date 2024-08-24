from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from fake_db.db import NEWS_TABLE
from schema.db.news import NewsSchema


class NewsRepository:
    def read_all(self, db: AsyncSession, **kwargs) -> List[NewsSchema]:
        return [NewsSchema(**news_item) for news_item in NEWS_TABLE]
