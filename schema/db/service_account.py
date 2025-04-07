from datetime import datetime

from pydantic import BaseModel, Field


class BaseServiceAccountSchema(BaseModel):
    name: str = Field(description="Service account name")
    token: str = Field(description="Service account token")
    token_valid_date: datetime = Field(description="Service account token valid date")


class ServiceAccountSchema(BaseServiceAccountSchema):
    id: int = Field(description="ID")
