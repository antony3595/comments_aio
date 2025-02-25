import asyncio
import logging
from typing import List

__all__ = ["remove_expired_service_accounts_task"]

from db.connections.postgres_null_pool import get_null_pool_async_session

from repository.service_account import get_service_account_repository

from tasks.celery import app


@app.task(queue="expired_service_accounts")
def remove_expired_service_accounts_task():
    logging.info(f"processing removing expired service accounts")
    res = asyncio.run(remove_expired_service_accounts())
    logging.info(f"expired accounts successfully removed")
    return res


async def remove_expired_service_accounts() -> List[int]:
    async with get_null_pool_async_session() as db:
        service_account_repository = get_service_account_repository()

        expired_service_accounts = await service_account_repository.read_expired_service_accounts(db)

        removed_service_accounts_ids = []
        for expired_service_account in expired_service_accounts:
            logging.info(f"removing expired service account: id={expired_service_account.id}")
            result = await service_account_repository.remove_by_id(db, expired_service_account.id)
            removed_service_accounts_ids.append(result)
        return removed_service_accounts_ids
