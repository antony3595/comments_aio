from pydantic import EmailStr, BaseModel

from schema.db.user import UserFields


class UserEmailQuery(BaseModel):
    email: EmailStr = UserFields.email
