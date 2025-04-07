from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import ServiceAccount
from schema.db.service_account import ServiceAccountSchema


class ServiceAccountRepository:
    async def read_by_token(self, db: AsyncSession, token: str) -> ServiceAccountSchema | None:
        stmt = select(ServiceAccount).where(ServiceAccount.token == token)
        result = await db.execute(stmt)
        account = result.scalars().one_or_none()
        return ServiceAccountSchema.model_validate(account, from_attributes=True) if account else None
