from typing import List

from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

import config
from db.connections.postgres import get_async_session
from repository.enums.scope import Scope
from schema.db.user import UserSchema
from services.auth.authorizaton import AuthService, get_auth_service
from services.auth.exceptions import AuthorizationException, AuthenticationException


class ApiKeyAuth:
    def __init__(self, api_key: str = Depends(APIKeyHeader(name="X-API-KEY", scheme_name="X-API-KEY"))):
        if api_key != config.settings.API_KEY.get_secret_value():
            raise HTTPException(status_code=403, detail="Invalid API key")


async def jwt_token_auth(token: str = Security(APIKeyHeader(name="Authorization", scheme_name="Token")),
                         auth_service: AuthService = Depends(get_auth_service),
                         db: AsyncSession = Depends(get_async_session)
                         ) -> UserSchema:
    try:
        user = await auth_service.validate_token(db, token, [])
        return user
    except AuthorizationException as e:
        raise HTTPException(detail=e.message, status_code=401)

    except AuthenticationException as e:
        raise HTTPException(detail=e.message, status_code=403)


class JWTTokenScopeAuth:
    def __init__(self, required_scope: List[Scope] = None):
        self.required_scope = required_scope

    async def __call__(self, token: str = Security(APIKeyHeader(name="Authorization", scheme_name="Token")),
                       db: AsyncSession = Depends(get_async_session),
                       auth_service: AuthService = Depends(get_auth_service),
                       ) -> UserSchema:

        try:
            user = await auth_service.validate_token(db, token, required_scope=self.required_scope)
            return user

        except AuthorizationException as e:
            raise HTTPException(detail=e.message, status_code=401)

        except AuthenticationException as e:
            raise HTTPException(detail=e.message, status_code=403)
