import logging

from fastapi import APIRouter, Depends, Body

from api.dependencies.auth import ApiKeyAuth
from repository.user import UserRepository
from schema.api.auth import UserTokenResponse, UserTokenRequest, BaseTokenPayload
from schema.db.user import UserSchema
from schema.query.user import UserEmailQuery
from services.auth.authorizaton import AuthService

logger = logging.getLogger(__name__)
auth_router = APIRouter(prefix="/auth")


@auth_router.post("/", response_model=UserTokenResponse, dependencies=[Depends(ApiKeyAuth)])
async def auth(data: UserTokenRequest = Body(),
               user_repository: UserRepository = Depends(UserRepository)) -> UserTokenResponse:
    db_query = UserEmailQuery(email=data.email)
    user = user_repository.read(db_query)

    if not user:
        user = user_repository.create(query=UserSchema(
            email=data.email,
            full_name=data.full_name,
        ))

    token = AuthService().generate_token(
        payload=BaseTokenPayload(id=user.id, **data.model_dump(exclude={"seconds"})),
        ttl=data.seconds)

    logger.info(f"Token generated for \"{data.model_dump_json()}\" request body")

    return UserTokenResponse(token=token)
