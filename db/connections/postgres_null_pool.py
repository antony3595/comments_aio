from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from config import settings

engine = create_async_engine(
    settings.DB_CONNECTION_STRING.get_secret_value(),
    echo=settings.DEBUG,
    poolclass=NullPool,
)
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autobegin=False,
)


@asynccontextmanager
async def get_null_pool_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
