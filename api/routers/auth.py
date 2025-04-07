import logging

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import ApiKeyAuth
from db.connections.postgres import get_db
from schema.api.auth import UserTokenResponse, UserTokenRequest, BaseTokenPayload
from schema.db.user import UserBaseSchema
from schema.query.user import UserReadQuery
from services.auth.authorizaton import AuthService
from services.users.users_service import get_user_service

logger = logging.getLogger(__name__)
auth_router = APIRouter(prefix="/auth")


@auth_router.post("/", response_model=UserTokenResponse, dependencies=[Depends(ApiKeyAuth)])
async def auth(data: UserTokenRequest = Body(),
               db: AsyncSession = Depends(get_db)) -> UserTokenResponse:
    user_service = get_user_service()

    db_query = UserReadQuery(email=data.email)
    user = await user_service.get_user(db, db_query)

    if not user:
        user_data = UserBaseSchema(
            email=data.email,
            full_name=data.full_name,
        )
        user = await user_service.create(db, payload=user_data)

    token = AuthService().generate_token(
        payload=BaseTokenPayload(id=user.id,
                                 **data.model_dump(include={"full_name", "email", "scope"})),
        ttl=data.seconds)

    logger.info(f"Token generated for \"{data.model_dump_json()}\" request body")

    return UserTokenResponse(token=token)
