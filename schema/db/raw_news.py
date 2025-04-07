from typing import Any, Dict

from pydantic import BaseModel, Field


class BaseRawNewsSchema(BaseModel):
    data: Dict[str, Any] = Field(description="JSON data")
    service_account_id: int = Field(description="Creator account ID")
    processed: bool | None = Field(description="Is data processed?", default=False)


class RawNewsSchema(BaseRawNewsSchema):
    id: int = Field(description="ID")


class CreateRawNewsSchema(BaseRawNewsSchema):
    ...


class UpdateRawNewsSchema(BaseModel):
    data: Dict[str, Any] | None = Field(description="JSON data", default=None)
    service_account_id: int | None = Field(description="Creator account ID", default=None)
    processed: bool | None = Field(description="Is data processed?", default=None)
