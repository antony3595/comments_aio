from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from repository.news import NewsRepository
from schema.db.base import PaginationSchema
from schema.db.news import NewsSchema, NewsWithCategoriesSchema, NewsCategorySubscribeValues, UserCategorySubscriptionSchema, \
    UserSubscriptionNewsQuery


class NewsService:
    @staticmethod
    async def read_all(db: AsyncSession) -> List[NewsSchema]:
        async with db.begin():
            result = await NewsRepository().read_all(db)
            await db.commit()
            return result

    @staticmethod
    async def read_all_extended(db: AsyncSession) -> List[NewsWithCategoriesSchema]:
        async with db.begin():
            result = await NewsRepository().read_all_extended(db)
            await db.commit()
            return result

    @staticmethod
    async def subscribe_to_category(db: AsyncSession, values: NewsCategorySubscribeValues) -> List[UserCategorySubscriptionSchema]:
        async with db.begin():
            result = await NewsRepository().subscribe_to_category(db=db, values=values)
            await db.commit()
            return result

    @staticmethod
    async def get_user_subscriptions(db: AsyncSession, query: UserSubscriptionNewsQuery, pagination: PaginationSchema = None) \
            -> List[NewsWithCategoriesSchema]:
        async with db.begin():
            result = await NewsRepository().get_user_subscription_news(db=db, query=query, pagination=pagination)
            await db.commit()
            return result


def get_news_service() -> NewsService:
    return NewsService()
