from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_async_engine(settings.DB_CONNECTION_STRING.get_secret_value(), echo=settings.DEBUG, pool_size=40, max_overflow=20)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
