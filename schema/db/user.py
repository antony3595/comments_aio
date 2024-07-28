from dataclasses import dataclass
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field


@dataclass
class UserFields:
    id: str = Field(default_factory=lambda: uuid4().hex)
    full_name: str = Field(description="Username")
    email: EmailStr = Field(description="Email address")


class UserSchema(BaseModel):
    id: str = UserFields.id
    email: EmailStr = UserFields.email
    full_name: str = UserFields.full_name
