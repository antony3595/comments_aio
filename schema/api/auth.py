from typing import List

from pydantic import EmailStr, Field, field_validator, ValidationError, BaseModel

import conf
from repository.enums.scope import Scope
from schema.db.user import UserFields


class UserTokenRequest(BaseModel):
    full_name: str = UserFields.full_name
    email: EmailStr = UserFields.email
    minutes: int = Field(description="TTL in minutes", default=30)
    scope: List[Scope] = Field(description="Token access scope")

    @field_validator("minutes")
    def minutes_not_greater_than_max_ttl(cls, value: int):
        if value > conf.settings.TOKEN_MAX_TTL:
            raise ValidationError("TTL cant be greater than {}".format(conf.settings.TOKEN_MAX_TTL))
        return value


class BaseTokenPayload(BaseModel):
    id: str = UserFields.id
    full_name: str = UserFields.full_name
    email: EmailStr = UserFields.email
    scope: List[Scope] = Field(description="Token access scope")


class TokenPayload(BaseTokenPayload):
    exp: float = Field(description="Expiration datetime")


class UserTokenResponse(BaseModel):
    token: str
