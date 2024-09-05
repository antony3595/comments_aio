from pydantic import BaseModel, EmailStr, Field


class UserFields:
    id: int = Field(description="Unique ID")
    full_name: str = Field(description="Username")
    email: EmailStr = Field(description="Email address")


class UserBaseSchema(BaseModel):
    email: EmailStr = UserFields.email
    full_name: str = UserFields.full_name


class UserSchema(UserBaseSchema):
    id: int = UserFields.id
