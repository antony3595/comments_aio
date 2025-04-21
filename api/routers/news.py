import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, Body

from api.dependencies.auth import JWTTokenScopeAuth
from db.connections.postgres import DBDependency
from repository.enums.scope import Scope
from schema.db.base import PaginationSchema
from schema.db.news import (
    NewsSchema,
    NewsWithCategoriesSchema,
    NewsCategorySubscribeRequestSchema,
    NewsCategorySubscribeValues,
    UserCategorySubscriptionSchema,
    UserSubscriptionNewsQuery,
)
from schema.db.user import UserSchema
from services.news.news_service import get_news_service
from services.users.users_service import get_user_service

logger = logging.getLogger(__name__)
news_router = APIRouter(prefix="/news")


@news_router.get("/", response_model=list[NewsSchema])
async def get_news(
    db: DBDependency,
    user: Annotated[
        UserSchema, Depends(JWTTokenScopeAuth(required_scope=[Scope.NEWS]))
    ],
) -> list[NewsSchema]:
    logger.info(f"User {user.email} got news response")
    news_service = get_news_service()
    return await news_service.read_all(db)


@news_router.get("/extended", response_model=list[NewsWithCategoriesSchema])
async def get_news_full(
    db: DBDependency,
    user: Annotated[
        UserSchema, Depends(JWTTokenScopeAuth(required_scope=[Scope.NEWS]))
    ],
) -> list[NewsWithCategoriesSchema]:
    logger.info(f"User {user.email} got extended news response")
    news_service = get_news_service()
    return await news_service.read_all_extended(db)


@news_router.post(
    "/subscribe", response_model=List[UserCategorySubscriptionSchema]
)
async def subscribe_user_to_category(
    db: DBDependency,
    user: Annotated[
        UserSchema, Depends(JWTTokenScopeAuth(required_scope=[Scope.NEWS]))
    ],
    body: NewsCategorySubscribeRequestSchema = Body(),
) -> List[UserCategorySubscriptionSchema]:
    service = get_news_service()
    values = NewsCategorySubscribeValues(
        user_id=user.id, categories=body.categories
    )
    result = await service.subscribe_to_category(db, values)
    return result


@news_router.get(
    "/subscriptions", response_model=List[NewsWithCategoriesSchema]
)
async def get_user_subscription_news(
    db: DBDependency,
    user: Annotated[
        UserSchema, Depends(JWTTokenScopeAuth(required_scope=[Scope.NEWS]))
    ],
    pagination: PaginationSchema = Depends(),
) -> List[NewsWithCategoriesSchema]:
    subscriptions = await get_user_service().get_subscriptions(db, user.id)
    categories = [subscription.category for subscription in subscriptions]
    news = await get_news_service().get_user_subscriptions(
        db,
        query=UserSubscriptionNewsQuery(categories=categories, user_id=user.id),
        pagination=pagination,
    )
    return news
