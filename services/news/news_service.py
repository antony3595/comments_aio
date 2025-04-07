from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.news import NewsTypeEnum
from repository.news import get_news_repository
from repository.news_category import get_news_category_repository
from schema.db.base import PaginationSchema
from schema.db.news import (
    NewsSchema,
    NewsWithCategoriesSchema,
    NewsCategorySubscribeValues,
    UserCategorySubscriptionSchema,
    UserSubscriptionNewsQuery,
    CreateNewsSchema,
)
from schema.db.news_category import CreateNewsCategoriesSchema
from schema.db.raw_news import RawNewsSchema
from schema.db.user import UserSchema


class NewsService:
    @staticmethod
    async def read_all(db: AsyncSession) -> List[NewsSchema]:
        async with db.begin():
            result = await get_news_repository().read_all(db)
            await db.commit()
            return result

    @staticmethod
    async def read_all_extended(
        db: AsyncSession,
    ) -> List[NewsWithCategoriesSchema]:
        async with db.begin():
            result = await get_news_repository().read_all_extended(db)
            await db.commit()
            return result

    @staticmethod
    async def subscribe_to_category(
        db: AsyncSession, values: NewsCategorySubscribeValues
    ) -> List[UserCategorySubscriptionSchema]:
        async with db.begin():
            result = await get_news_repository().subscribe_to_category(
                db=db, values=values
            )
            await db.commit()
            return result

    @staticmethod
    async def get_user_subscriptions(
        db: AsyncSession,
        query: UserSubscriptionNewsQuery,
        pagination: PaginationSchema = None,
    ) -> List[NewsWithCategoriesSchema]:
        async with db.begin():
            result = await get_news_repository().get_user_subscription_news(
                db=db, query=query, pagination=pagination
            )
            await db.commit()
            return result

    async def create(
        self, db: AsyncSession, news_values: CreateNewsSchema
    ) -> NewsSchema:
        async with db.begin():
            result = await get_news_repository().create(
                db=db, values=news_values
            )
            await db.commit()
            return result

    async def create_from_raw_news(
        self, db: AsyncSession, raw_news: RawNewsSchema
    ) -> NewsWithCategoriesSchema | None:
        news_repository = get_news_repository()
        async with db.begin():
            categories = raw_news.data.pop("categories", [])
            news_values = CreateNewsSchema.model_validate(raw_news.data)
            news = await news_repository.create(db=db, values=news_values)

            news_categories_values = CreateNewsCategoriesSchema(
                news_id=news.id, categories=categories
            )
            await get_news_category_repository().create(
                db, news_categories_values
            )
            await db.commit()

        async with db.begin():
            res = await news_repository.read_extended_by_id(db, news.id)
            await db.commit()
            return res

    async def get_subsribers_by_categories(
        self, db: AsyncSession, categories: List[NewsTypeEnum]
    ) -> List[UserSchema]:
        news_categories_repository = get_news_category_repository()
        async with db.begin():
            subscribers = await news_categories_repository.get_subscribed_users(
                db=db, categories=categories
            )
            await db.commit()
            return subscribers


def get_news_service() -> NewsService:
    return NewsService()
