import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import JWTTokenScopeAuth
from db.connections.postgres import get_async_session
from repository.enums.scope import Scope
from repository.news import NewsRepository
from schema.db.news import NewsSchema
from schema.db.user import UserSchema

logger = logging.getLogger(__name__)
news_router = APIRouter(prefix="/news")


@news_router.get("/", response_model=list[NewsSchema])
async def get_news(
        user: Annotated[UserSchema, Depends(JWTTokenScopeAuth(required_scope=[Scope.NEWS]))],
        db: AsyncSession = Depends(get_async_session)) -> list[NewsSchema]:
    logger.info(f"User {user.email} got news response")
    return await NewsRepository().read_all(db)
