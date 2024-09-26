from typing import List

from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

import config
from db.connections.postgres import get_async_session
from repository.enums.scope import Scope
from repository.user import UserRepository, get_user_repository
from schema.db.user import UserSchema
from schema.query.user import UserReadQuery
from services.auth.authorizaton import AuthService, get_auth_service
from services.auth.exceptions import AuthorizationException, AuthenticationException


class ApiKeyAuth:
    def __init__(self, api_key: str = Security(APIKeyHeader(name="Authorization"))):
        if api_key != config.settings.API_KEY.get_secret_value():
            raise HTTPException(status_code=403, detail="Invalid API key")


async def jwt_token_auth(token: str = Security(APIKeyHeader(name="Authorization")),
                         auth_service: AuthService = Depends(get_auth_service),
                         user_repository: UserRepository = Depends(get_user_repository)
                         ) -> UserSchema:
    auth_service.validate_token(token, [])
    token_payload = auth_service.parse_token(token)

    user = user_repository.read(query=UserReadQuery(email=token_payload.email))
    if not user:
        raise HTTPException(detail="No user with given token", status_code=403)

    return user


class JWTTokenScopeAuth:
    def __init__(self, required_scope: List[Scope]):
        self.required_scope = required_scope

    async def __call__(self, db: AsyncSession = Depends(get_async_session), token: str = Security(APIKeyHeader(name="Authorization")),
                 token_service: AuthService = Depends(get_auth_service),
                 user_repository: UserRepository = Depends(get_user_repository)
                 ):

        try:
            token_service.validate_token(db, token, required_scope=self.required_scope)
            token_payload = token_service.parse_token(token)

        except AuthorizationException as e:
            raise HTTPException(detail=e.message, status_code=401)

        except AuthenticationException as e:
            raise HTTPException(detail=e.message, status_code=403)

        user = await user_repository.read(db, query=UserReadQuery(email=token_payload.email))
        if not user:
            raise HTTPException(detail="No user with given token", status_code=403)

        return user
