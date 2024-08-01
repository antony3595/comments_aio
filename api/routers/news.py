import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies.auth import JWTTokenScopeAuth
from repository.enums.scope import Scope
from repository.news import NewsRepository
from schema.db.news import NewsSchema
from schema.db.user import UserSchema

logger = logging.getLogger(__name__)
news_router = APIRouter(prefix="/news")


@news_router.get("/", response_model=list[NewsSchema])
async def get_news(user: Annotated[UserSchema, Depends(JWTTokenScopeAuth(required_scope=[Scope.NEWS]))]):
    logger.info(f"User {user.email} got news response")
    return NewsRepository().read_all()
