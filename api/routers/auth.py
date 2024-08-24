import logging

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import ApiKeyAuth
from db.connections.postgres import get_async_session
from repository.user import UserRepository
from schema.api.auth import UserTokenResponse, UserTokenRequest, BaseTokenPayload
from schema.db.user import UserBaseSchema
from schema.query.user import UserEmailQuery
from services.auth.authorizaton import AuthService

logger = logging.getLogger(__name__)
auth_router = APIRouter(prefix="/auth")


@auth_router.post("/", response_model=UserTokenResponse, dependencies=[Depends(ApiKeyAuth)])
async def auth(data: UserTokenRequest = Body(),
               db: AsyncSession = Depends(get_async_session),
               user_repository: UserRepository = Depends(UserRepository)) -> UserTokenResponse:
    db_query = UserEmailQuery(email=data.email)
    user = await user_repository.read(db, db_query)

    if not user:
        user = await user_repository.create(db, query=UserBaseSchema(
            email=data.email,
            full_name=data.full_name,
        ))

    token = AuthService().generate_token(
        payload=BaseTokenPayload(id=user.id, **data.model_dump(exclude={"seconds"})),
        ttl=data.seconds)

    logger.info(f"Token generated for \"{data.model_dump_json()}\" request body")

    return UserTokenResponse(token=token)
