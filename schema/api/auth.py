from typing import List

from fastapi.exceptions import RequestValidationError
from pydantic import EmailStr, Field, field_validator, BaseModel

import config
from repository.enums.scope import Scope
from schema.db.user import UserFields


class UserTokenRequest(BaseModel):
    full_name: str = UserFields.full_name
    email: EmailStr = UserFields.email
    seconds: int = Field(description="TTL in seconds", default=3600)
    scope: List[Scope] = Field(description="Token access scope")

    @field_validator("seconds")
    def is_token_ttl_valid(cls, value: int):
        if value > config.settings.TOKEN_MAX_TTL:
            raise RequestValidationError("TTL cant be greater than {}".format(config.settings.TOKEN_MAX_TTL))
        return value


class BaseTokenPayload(BaseModel):
    id: int = UserFields.id
    full_name: str = UserFields.full_name
    email: EmailStr = UserFields.email
    scope: List[Scope] = Field(description="Token access scope")


class TokenPayload(BaseTokenPayload):
    exp: float = Field(description="Expiration datetime")


class UserTokenResponse(BaseModel):
    token: str
