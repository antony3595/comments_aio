from datetime import datetime

from pydantic import BaseModel, Field


class NewsFields:
    id: int = Field()
    title: str = Field(description="Title")
    created_at: datetime = Field(description="Created at")


class NewsSchema(BaseModel):
    id: int = NewsFields.id
    title: str = NewsFields.title
    created_at: datetime = NewsFields.created_at
