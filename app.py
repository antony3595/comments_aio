import logging

from fastapi import FastAPI, Header, HTTPException, Body, Security
from fastapi.security import APIKeyHeader

import conf
from repository.enums.scope import Scope
from repository.news import NewsRepository
from schema.api.auth import UserTokenRequest, UserTokenResponse, BaseTokenPayload
from schema.db.user import UserSchema
from schema.query.user import UserEmailQuery
from repository.user import UserRepository
from services.auth.token import TokenService

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def root(api_key: str = Header()):
    if api_key != conf.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return {"message": "Hello World"}


@app.post("/auth", response_model=UserTokenResponse)
async def auth(data: UserTokenRequest = Body(), api_key: str = Header()):
    if api_key != conf.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    db_query = UserEmailQuery(email=data.email)
    repo = UserRepository()

    user = repo.read(db_query)

    if not user:
        user = repo.create(query=UserSchema(
            email=data.email,
            full_name=data.full_name,
        ))

    token_payload = BaseTokenPayload(id=user.id, **data.model_dump(exclude={"minutes"}))
    token = TokenService().generate_token(token_payload, data.minutes)

    logger.info(f"Token generated for \"{data.model_dump_json()}\" request body")

    return UserTokenResponse(token=token)


@app.get("/news", )
async def get_news(authorization: str = Security(APIKeyHeader(name="Authorization"))):
    token_service = TokenService()
    token_service.validate_token(authorization, [Scope.NEWS])
    token_payload = token_service.get_token_payload(authorization)

    logger.info(f"User {token_payload.id} got news response")

    return NewsRepository().read_all()
