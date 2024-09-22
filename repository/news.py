from typing import List

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models.news import News, NewsCategory, UserCategorySubscription
from schema.db.news import NewsSchema, NewsWithCategoriesSchema, NewsCategorySubscribeValues, UserCategorySubscriptionSchema


class NewsRepository:
    async def read_all(self, db: AsyncSession, **kwargs) -> List[NewsSchema]:
        stmt = await db.execute(select(News))
        news = stmt.scalars().all()

        return [NewsSchema.model_validate(news_item, from_attributes=True) for news_item in news]

    async def read_all_extended(self, db: AsyncSession, **kwargs) -> List[NewsWithCategoriesSchema]:
        stmt = await db.execute(select(News).options(joinedload(News.categories).load_only(NewsCategory.category)))
        news = stmt.scalars().unique()

        return [NewsWithCategoriesSchema.model_validate(news_item, from_attributes=True) for news_item in news]

    async def subscribe_to_category(self, db: AsyncSession, values: NewsCategorySubscribeValues) -> List[UserCategorySubscriptionSchema]:
        await db.execute(delete(UserCategorySubscription).where(UserCategorySubscription.user_id == values.user_id))
        dict_values = [{'user_id': values.user_id, 'category': category} for category in values.categories]

        subscriptions = await db.execute(insert(UserCategorySubscription).values(dict_values).returning(UserCategorySubscription))
        result = [UserCategorySubscriptionSchema.model_validate(s, from_attributes=True) for s in subscriptions.scalars().all()]
        return result
