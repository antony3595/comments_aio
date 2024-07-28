import logging
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException, Body, Depends

import conf
from api.dependencies.auth import ApiKeyAuth, JWTTokenScopeAuth
from repository.enums.scope import Scope
from repository.news import NewsRepository
from repository.user import UserRepository
from schema.api.auth import UserTokenRequest, UserTokenResponse, BaseTokenPayload
from schema.db.user import UserSchema
from schema.query.user import UserEmailQuery
from services.auth.token import TokenService

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def root(api_key: str = Header()):
    if api_key != conf.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return {"message": "Hello World"}


@app.post("/auth", response_model=UserTokenResponse, dependencies=[Depends(ApiKeyAuth)])
async def auth(data: UserTokenRequest = Body(),
               user_repository: UserRepository = Depends(UserRepository)):
    db_query = UserEmailQuery(email=data.email)
    user = user_repository.read(db_query)

    if not user:
        user = user_repository.create(query=UserSchema(
            email=data.email,
            full_name=data.full_name,
        ))

    token = TokenService().generate_token(
        payload=BaseTokenPayload(id=user.id, **data.model_dump(exclude={"minutes"})),
        ttl=data.minutes)

    logger.info(f"Token generated for \"{data.model_dump_json()}\" request body")

    return UserTokenResponse(token=token)


@app.get("/news", )
async def get_news(user: Annotated[UserSchema, Depends(JWTTokenScopeAuth(required_scope=[Scope.NEWS]))]):
    logger.info(f"User {user.email} got news response")
    return NewsRepository().read_all()
