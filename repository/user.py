from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import AuthUser
from schema.db.user import UserSchema, UserBaseSchema
from schema.query.user import UserEmailQuery


class UserRepository:
    async def read(self, db: AsyncSession, query: UserEmailQuery) -> UserSchema | None:
        stmt = await db.execute(select(AuthUser).where(AuthUser.email == query.email))
        user = stmt.scalars().one_or_none()
        return UserSchema.model_validate(user, from_attributes=True) if user else None

    async def create(self, db: AsyncSession, query: UserBaseSchema) -> UserSchema | None:
        stmt = await db.execute(insert(AuthUser).returning(AuthUser), query.model_dump())
        user = stmt.scalars().one_or_none()
        await db.commit()
        return UserSchema.model_validate(user, from_attributes=True) if user else None


def get_user_repository() -> UserRepository:
    return UserRepository()
