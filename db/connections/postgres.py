from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from config import settings

engine = create_async_engine(
    settings.DB_CONNECTION_STRING.get_secret_value(),
    echo=settings.DEBUG,
    pool_size=40,
    max_overflow=20,
)
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autobegin=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


DBDependency = Annotated[AsyncSession, Depends(get_db)]
