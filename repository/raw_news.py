from typing import List

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.news import RawNews
from schema.db.base import PaginationSchema
from schema.db.raw_news import CreateRawNewsSchema, RawNewsSchema, UpdateRawNewsSchema, RawNewsFiltersSchema


class RawNewsRepository:
    async def create(self, db: AsyncSession, data: CreateRawNewsSchema) -> RawNewsSchema:
        stmt = insert(RawNews).values(data.model_dump()).returning(RawNews)
        result = await db.execute(stmt)
        raw_news = result.scalars().one()
        return RawNewsSchema.model_validate(raw_news, from_attributes=True)

    async def read(self, db: AsyncSession, raw_news_id: int) -> RawNewsSchema:
        stmt = select(RawNews).where(RawNews.id == raw_news_id)
        result = await db.execute(stmt)
        result = result.scalars().one()
        return RawNewsSchema.model_validate(result, from_attributes=True) if result else None

    async def read_all(self, db: AsyncSession,
                       filters: RawNewsFiltersSchema = None,
                       pagination: PaginationSchema = None) -> List[RawNewsSchema]:

        stmt = select(RawNews)
        if filters:
            stmt = stmt.filter_by(**filters.to_orm_filters())
        if pagination:
            stmt = stmt.limit(pagination.size).offset((pagination.page - 1) * pagination.size)
        db_result = await db.execute(stmt)
        result = db_result.scalars().all()
        return [RawNewsSchema.model_validate(item, from_attributes=True) for item in result] if result else []

    async def update(self, db: AsyncSession, raw_news_id: int, values: UpdateRawNewsSchema) -> RawNewsSchema:
        stmt = update(RawNews).where(RawNews.id == raw_news_id).values(values.model_dump(exclude_unset=True)).returning(RawNews)
        result = await db.execute(stmt)
        result = result.scalars().one()
        return RawNewsSchema.model_validate(result, from_attributes=True)

    async def create_bulk(self, db, data: List[CreateRawNewsSchema]) -> List[RawNewsSchema]:
        dict_values = [data_item.model_dump() for data_item in data]

        stmt = insert(RawNews).values(dict_values).returning(RawNews)
        result = await db.execute(stmt)
        raw_news = result.scalars().all()
        return [RawNewsSchema.model_validate(raw_news_item, from_attributes=True) for raw_news_item in raw_news]


def get_raw_news_repository() -> RawNewsRepository:
    return RawNewsRepository()
