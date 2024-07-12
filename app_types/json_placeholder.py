from typing import Optional

from pydantic import BaseModel, PositiveInt, Field


class Post(BaseModel):
    userId: PositiveInt
    id: PositiveInt
    title: str
    body: str


class PostPatchDTO(BaseModel):
    id: PositiveInt
    userId: Optional[PositiveInt] = Field(default=None)
    title: Optional[str] = Field(default=None)
    body: Optional[str] = Field(default=None)


class Comment(BaseModel):
    postId: PositiveInt
    id: PositiveInt
    name: str
    email: str
    body: str
