from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from repository.user import UserRepository
from schema.db.news import UserCategorySubscriptionSchema
from schema.db.user import UserSchema, UserBaseSchema
from schema.query.user import UserReadQuery


class UsersService:
    async def get_user(
        self, db: AsyncSession, query: UserReadQuery
    ) -> UserSchema:
        async with db.begin():
            user = await UserRepository().read(db, query)
            await db.commit()
            return user

    async def create(
        self, db: AsyncSession, payload: UserBaseSchema
    ) -> UserSchema:
        async with db.begin():
            user = await UserRepository().create(db, payload)
            await db.commit()
            return user

    async def get_subscriptions(
        self, db: AsyncSession, user_id: int
    ) -> List[UserCategorySubscriptionSchema]:
        async with db.begin():
            user = await UserRepository().get_subscriptions(db, user_id)
            await db.commit()
            return user


def get_user_service() -> UsersService:
    return UsersService()
