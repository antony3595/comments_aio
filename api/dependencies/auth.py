from typing import List

from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader

import conf
from repository.enums.scope import Scope
from repository.user import UserRepository, get_user_repository
from schema.db.user import UserSchema
from schema.query.user import UserEmailQuery
from services.auth.token import TokenService, get_token_service


class ApiKeyAuth:
    def __init__(self, api_key: str = Security(APIKeyHeader(name="Authorization"))):
        if api_key != conf.settings.API_KEY.get_secret_value():
            raise HTTPException(status_code=403, detail="Invalid API key")


async def jwt_token_auth(token: str = Security(APIKeyHeader(name="Authorization")),
                         token_service: TokenService = Depends(get_token_service),
                         user_repository: UserRepository = Depends(get_user_repository)
                         ) -> UserSchema:
    token_service.validate_token(token, [])
    token_payload = token_service.parse_token(token)

    user = user_repository.read(query=UserEmailQuery(email=token_payload.email))
    if not user:
        raise HTTPException(detail="No user with given token", status_code=403)

    return user


class JWTTokenScopeAuth:
    def __init__(self, required_scope: List[Scope]):
        self.required_scope = required_scope

    def __call__(self, token: str = Security(APIKeyHeader(name="Authorization")),
                 token_service: TokenService = Depends(get_token_service),
                 user_repository: UserRepository = Depends(get_user_repository)
                 ):
        token_service.validate_token(token, required_scope=self.required_scope)
        token_payload = token_service.parse_token(token)

        user = user_repository.read(query=UserEmailQuery(email=token_payload.email))
        if not user:
            raise HTTPException(detail="No user with given token", status_code=403)

        return user
