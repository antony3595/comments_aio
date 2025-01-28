import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import JWTTokenScopeAuth
from db.connections.postgres import get_async_session
from repository.enums.scope import Scope
from repository.news import NewsRepository
from repository.user import UserRepository
from schema.db.base import PaginationSchema
from schema.db.news import NewsSchema, NewsWithCategoriesSchema, NewsCategorySubscribeRequestSchema, NewsCategorySubscribeValues, \
    UserCategorySubscriptionSchema, UserSubscriptionNewsQuery
from schema.db.user import UserSchema

logger = logging.getLogger(__name__)
news_router = APIRouter(prefix="/news")


@news_router.get("/", response_model=list[NewsSchema])
async def get_news(
        user: Annotated[UserSchema, Depends(JWTTokenScopeAuth(required_scope=[Scope.NEWS]))],
        db: AsyncSession = Depends(get_async_session)) -> list[NewsSchema]:
    logger.info(f"User {user.email} got news response")
    return await NewsRepository().read_all(db)


@news_router.get("/extended", response_model=list[NewsWithCategoriesSchema])
async def get_news_full(
        user: Annotated[UserSchema, Depends(JWTTokenScopeAuth(required_scope=[Scope.NEWS]))],
        db: AsyncSession = Depends(get_async_session)) -> list[NewsWithCategoriesSchema]:
    logger.info(f"User {user.email} got news response")
    return await NewsRepository().read_all_extended(db)


@news_router.post("/subscribe", response_model=List[UserCategorySubscriptionSchema])
async def subscribe_user_to_category(user: Annotated[UserSchema, Depends(JWTTokenScopeAuth(required_scope=[Scope.NEWS]))],
                                     db: AsyncSession = Depends(get_async_session),
                                     body: NewsCategorySubscribeRequestSchema = Body()
                                     ) -> List[UserCategorySubscriptionSchema]:
    values = NewsCategorySubscribeValues(user_id=user.id, categories=body.categories)
    result = await NewsRepository().subscribe_to_category(db, values)
    return result


@news_router.get("/subscriptions", response_model=List[NewsSchema])
async def get_user_subscription_news(user: Annotated[UserSchema, Depends(JWTTokenScopeAuth(required_scope=[Scope.NEWS]))],
                                     pagination: PaginationSchema = Depends(),
                                     db: AsyncSession = Depends(get_async_session),
                                     ) -> List[NewsSchema]:
    subscriptions = await UserRepository().get_subscriptions(db, user_id=user.id)
    categories = [subscription.category for subscription in subscriptions]

    news = await (NewsRepository().get_user_subscription_news(db,
                                                              query=UserSubscriptionNewsQuery(
                                                                  categories=categories,
                                                                  user_id=user.id),
                                                              pagination=pagination))
    return news
