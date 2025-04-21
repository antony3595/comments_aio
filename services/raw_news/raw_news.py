from typing import Dict, Any, List

from sqlalchemy.ext.asyncio import AsyncSession

from repository.raw_news import get_raw_news_repository, RawNewsRepository
from schema.db.base import PaginationSchema
from schema.db.raw_news import (
    CreateRawNewsSchema,
    RawNewsSchema,
    UpdateRawNewsSchema,
    RawNewsFiltersSchema,
)


class RawNewsService:
    @staticmethod
    async def create_raw_news(
        db: AsyncSession, service_account_id: int, raw_news_data: Dict[str, Any]
    ) -> RawNewsSchema:
        async with db.begin():
            data = CreateRawNewsSchema(
                service_account_id=service_account_id, data=raw_news_data
            )
            raw_news_repository = get_raw_news_repository()
            raw_news = await raw_news_repository.create(db, data)
            await db.commit()
            return raw_news

    async def read_all(
        self,
        db: AsyncSession,
        filters: RawNewsFiltersSchema | None = None,
        pagination: PaginationSchema | None = None,
    ) -> List[RawNewsSchema]:
        async with db.begin():
            res = await get_raw_news_repository().read_all(
                db, filters, pagination
            )
            await db.commit()
            return res

    @staticmethod
    async def get_by_id(db: AsyncSession, raw_news_id: int) -> RawNewsSchema:
        async with db.begin():
            raw_news = await RawNewsRepository().read(db, raw_news_id)
            await db.commit()
            return raw_news

    @staticmethod
    async def create_raw_news_bulk(
        db: AsyncSession,
        service_account_id: int,
        raw_news_data_values: List[Dict[str, Any]],
    ) -> List[RawNewsSchema]:
        async with db.begin():
            data = [
                CreateRawNewsSchema(
                    service_account_id=service_account_id, data=data_item
                )
                for data_item in raw_news_data_values
            ]
            raw_news_repository = get_raw_news_repository()
            raw_news = await raw_news_repository.create_bulk(db, data)
            await db.commit()
            return raw_news

    async def update(
        self, db: AsyncSession, raw_news_id: int, values: UpdateRawNewsSchema
    ) -> RawNewsSchema:
        async with db.begin():
            raw_news_repository = get_raw_news_repository()
            raw_news = await raw_news_repository.update(db, raw_news_id, values)
            await db.commit()
            return raw_news


def get_raw_news_service() -> RawNewsService:
    return RawNewsService()
