from typing import List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.news import NewsCategory, NewsTypeEnum, UserCategorySubscription
from db.models.user import AuthUser
from schema.db.news_category import (
    CreateNewsCategoriesSchema,
    NewsCategorySchema,
)
from schema.db.user import UserSchema


class NewsCategoryRepository:
    async def create(
        self, db: AsyncSession, values: CreateNewsCategoriesSchema
    ) -> List[NewsCategorySchema]:
        news_id = values.news_id
        categories = values.categories
        values = [
            {"news_id": news_id, "category": category}
            for category in categories
        ]

        stmt = insert(NewsCategory).values(values).returning(NewsCategory)
        db_result = await db.execute(stmt)
        news_categories = db_result.scalars().all()

        result = (
            [
                NewsCategorySchema.model_validate(
                    news_category, from_attributes=True
                )
                for news_category in news_categories
            ]
            if news_categories
            else []
        )

        return result

    async def get_subscribed_users(
        self, db: AsyncSession, categories: List[NewsTypeEnum]
    ) -> List[UserSchema]:
        stmt = (
            select(AuthUser)
            .join(UserCategorySubscription)
            .where(UserCategorySubscription.category.in_(categories))
        )
        db_result = await db.execute(stmt)
        users = db_result.scalars().unique()
        return [
            UserSchema.model_validate(user, from_attributes=True)
            for user in users
        ]


def get_news_category_repository() -> NewsCategoryRepository:
    return NewsCategoryRepository()
