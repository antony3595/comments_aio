from pydantic import BaseModel, PositiveInt, Field


class Post(BaseModel):
    userId: PositiveInt
    id: PositiveInt
    title: str
    body: str


class PostPatchDTO(BaseModel):
    id: PositiveInt
    userId: PositiveInt | None = Field(default=None)
    title: str | None = Field(default=None)
    body: str | None = Field(default=None)


class Comment(BaseModel):
    postId: PositiveInt
    id: PositiveInt
    name: str
    email: str
    body: str
