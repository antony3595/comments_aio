import asyncio
import logging

__all__ = ["remove_expired_service_accounts_task"]

from db.connections.postgres_null_pool import get_null_pool_async_session

from services.service_accounts.service_accounts import (
    get_service_accounts_service,
)

from tasks.celery import app


@app.task(queue="expired_service_accounts_queue")
def remove_expired_service_accounts_task():
    logging.info(f"processing removing expired service accounts")
    res = asyncio.run(remove_expired_service_accounts())
    logging.info(f"expired accounts successfully removed")
    return res


async def remove_expired_service_accounts() -> None:
    async with get_null_pool_async_session() as db:
        service_accounts_service = get_service_accounts_service()
        expired_service_accounts = (
            await service_accounts_service.get_expired_accounts(db)
        )

        for expired_service_account in expired_service_accounts:
            logging.info(
                f"removing expired service account: id={expired_service_account.id}"
            )
            await service_accounts_service.remove_by_id(
                db, expired_service_account.id
            )
