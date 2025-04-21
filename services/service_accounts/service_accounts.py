from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from repository.service_account import get_service_account_repository
from schema.db.service_account import ServiceAccountSchema


class ServiceAccountsService:
    async def get_expired_accounts(
        self, db: AsyncSession
    ) -> List[ServiceAccountSchema]:
        service_account_repository = get_service_account_repository()
        async with db.begin():
            accounts = (
                await service_account_repository.read_expired_service_accounts(
                    db
                )
            )
            await db.commit()
            return accounts

    async def remove_by_id(
        self, db: AsyncSession, account_id: int
    ) -> int | None:
        service_account_repository = get_service_account_repository()
        async with db.begin():
            removed_id = await service_account_repository.remove_by_id(
                db, account_id
            )
            await db.commit()
            return removed_id


def get_service_accounts_service() -> ServiceAccountsService:
    return ServiceAccountsService()
