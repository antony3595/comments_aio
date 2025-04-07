from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import ServiceAccount
from schema.db.service_account import ServiceAccountSchema


class ServiceAccountRepository:
    async def read_by_token(
        self, db: AsyncSession, token: str
    ) -> ServiceAccountSchema | None:
        stmt = select(ServiceAccount).where(ServiceAccount.token == token)
        result = await db.execute(stmt)
        account = result.scalars().one_or_none()
        return (
            ServiceAccountSchema.model_validate(account, from_attributes=True)
            if account
            else None
        )

    async def read_expired_service_accounts(
        self, db: AsyncSession
    ) -> list[ServiceAccountSchema]:
        stmt = select(ServiceAccount).where(
            ServiceAccount.token_valid_date <= func.now()
        )
        db_result = await db.execute(stmt)
        accounts = db_result.scalars().all()
        return (
            [
                ServiceAccountSchema.model_validate(acc, from_attributes=True)
                for acc in accounts
            ]
            if accounts
            else []
        )

    async def remove_by_id(
        self, db: AsyncSession, account_id: int
    ) -> int | None:
        stmt = (
            delete(ServiceAccount)
            .where(ServiceAccount.id == account_id)
            .returning(ServiceAccount.id)
        )
        db_result = await db.execute(stmt)
        removed_acc_id = db_result.scalars().one_or_none()
        return removed_acc_id


def get_service_account_repository() -> ServiceAccountRepository:
    return ServiceAccountRepository()
