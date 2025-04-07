from datetime import datetime
from typing import List

from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

import config
from db.connections.postgres import get_db
from repository.enums.scope import Scope
from repository.service_account import ServiceAccountRepository
from schema.db.service_account import ServiceAccountSchema
from schema.db.user import UserSchema
from services.auth.authorizaton import AuthService, get_auth_service
from services.auth.exceptions import (
    AuthorizationException,
    AuthenticationException,
)

token_header = APIKeyHeader(name="Authorization", scheme_name="Token")
api_key_header = APIKeyHeader(name="X-API-KEY", scheme_name="X-API-KEY")


class ApiKeyAuth:
    def __init__(self, api_key: str = Security(api_key_header)):
        if api_key != config.settings.API_KEY.get_secret_value():
            raise HTTPException(status_code=403, detail="Invalid API key")


async def jwt_token_auth(
    token: str = Security(token_header),
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_db),
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

    async def __call__(
        self,
        token: str = Security(token_header),
        db: AsyncSession = Depends(get_db),
        auth_service: AuthService = Depends(get_auth_service),
    ) -> UserSchema:

        try:
            user = await auth_service.validate_token(
                db, token, required_scope=self.required_scope
            )
            return user

        except AuthorizationException as e:
            raise HTTPException(detail=e.message, status_code=401)

        except AuthenticationException as e:
            raise HTTPException(detail=e.message, status_code=403)


class ServiceAccountAuth:
    async def __call__(
        self,
        token: str = Security(token_header),
        db: AsyncSession = Depends(get_db),
    ) -> ServiceAccountSchema:
        async with db.begin():
            service_account = await ServiceAccountRepository().read_by_token(
                db, token
            )
            await db.commit()
        if (
            service_account
            and service_account.token_valid_date > datetime.now()
        ):
            return service_account

        raise HTTPException(detail="Unauthorized", status_code=401)
