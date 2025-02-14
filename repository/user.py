from typing import List

from sqlalchemy import select, or_
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.news import UserCategorySubscription
from db.models.user import AuthUser
from schema.db.news import UserCategorySubscriptionSchema
from schema.db.user import UserSchema, UserBaseSchema
from schema.query.user import UserReadQuery


class UserRepository:
    async def read(self, db: AsyncSession, query: UserReadQuery) -> UserSchema | None:
        stmt = await db.execute(select(AuthUser).where(or_(AuthUser.email == query.email, AuthUser.id == query.id)))
        user = stmt.scalars().one_or_none()
        return UserSchema.model_validate(user, from_attributes=True) if user else None

    async def get_subscriptions(self, db: AsyncSession, user_id: int) -> List[UserCategorySubscriptionSchema]:
        stmt = await db.execute(select(UserCategorySubscription).where(UserCategorySubscription.user_id == user_id))
        subscriptions = stmt.scalars().all()

        return [UserCategorySubscriptionSchema.model_validate(subscription, from_attributes=True) for subscription in subscriptions]

    async def create(self, db: AsyncSession, query: UserBaseSchema) -> UserSchema | None:
        stmt = await db.execute(insert(AuthUser).returning(AuthUser), query.model_dump())
        user = stmt.scalars().one_or_none()
        return UserSchema.model_validate(user, from_attributes=True) if user else None


def get_user_repository() -> UserRepository:
    return UserRepository()
