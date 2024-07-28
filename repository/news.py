from typing import List

from fake_db.db import NEWS_TABLE
from repository.base import BaseRepository
from schema.db.news import NewsSchema


class NewsRepository(BaseRepository):
    def read_all(self, *args, **kwargs) -> List[NewsSchema]:
        return [NewsSchema(**news_item) for news_item in NEWS_TABLE]
