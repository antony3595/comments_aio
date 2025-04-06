from typing import List

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models.news import News, NewsCategory, UserCategorySubscription
from schema.db.base import PaginationSchema
from schema.db.news import NewsSchema, NewsWithCategoriesSchema, NewsCategorySubscribeValues, UserCategorySubscriptionSchema, \
    UserSubscriptionNewsQuery, CreateNewsSchema


class NewsRepository:
    async def create(self, db: AsyncSession, values: CreateNewsSchema, **kwargs) -> NewsSchema:
        stmt = insert(News).values(values.model_dump()).returning(News)
        result = await db.execute(stmt)
        news = result.scalars().one_or_none()
        return NewsSchema.model_validate(news, from_attributes=True)

    async def read_all(self, db: AsyncSession) -> List[NewsSchema]:
        stmt = await db.execute(select(News))
        news = stmt.scalars().all()

        return [NewsSchema.model_validate(news_item, from_attributes=True) for news_item in news]

    async def read_all_extended(self, db: AsyncSession) -> List[NewsWithCategoriesSchema]:
        # TODO сделать categories листом
        stmt = select(News).options(joinedload(News.categories, innerjoin=True).load_only(NewsCategory.category))
        result = await db.execute(stmt)
        news = result.scalars().unique()
        return [NewsWithCategoriesSchema.model_validate(news_item, from_attributes=True) for news_item in news]

    async def subscribe_to_category(self, db: AsyncSession, values: NewsCategorySubscribeValues) -> List[UserCategorySubscriptionSchema]:
        await db.execute(delete(UserCategorySubscription).where(UserCategorySubscription.user_id == values.user_id))
        dict_values = [{'user_id': values.user_id, 'category': category} for category in values.categories]

        subscriptions = await db.execute(insert(UserCategorySubscription).values(dict_values).returning(UserCategorySubscription))
        result = [UserCategorySubscriptionSchema.model_validate(s, from_attributes=True) for s in subscriptions.scalars().all()]
        return result

    async def get_user_subscription_news(self, db: AsyncSession, query: UserSubscriptionNewsQuery, pagination: PaginationSchema = None) -> \
            List[NewsWithCategoriesSchema]:
        # TODO узнать как оптимальнее, через join таблицы users_categories_subscriptions или так
        categories = [c.value for c in query.categories]
        stmt = (select(News)
                .join(NewsCategory)
                .options(joinedload(News.categories)
                         .load_only(NewsCategory.category))
                .where(NewsCategory.category.in_(categories))
                .order_by(News.created_at.desc()))
        # TODO сделать общую пагинацию, вместе с количеством элементов в Response
        if pagination:
            stmt = stmt.limit(pagination.size).offset((pagination.page - 1) * pagination.size)

        result = await db.execute(stmt)
        news = result.scalars().unique()
        result = [NewsWithCategoriesSchema.model_validate(news_item, from_attributes=True) for news_item in news]
        return result


def get_news_repository() -> NewsRepository:
    return NewsRepository()
