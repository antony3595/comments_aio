from pydantic import (
    EmailStr,
    BaseModel,
    model_validator,
    ValidationError,
)

from schema.db.user import UserFields


class UserReadQuery(BaseModel):
    id: int | None = None
    email: EmailStr | None = UserFields.email

    @model_validator(mode="before")
    @classmethod
    def validate_required_fields(cls, values):
        if not (values.get("id") or values.get("email")):
            raise ValidationError(f"'id' or 'email' required'")
        return values
