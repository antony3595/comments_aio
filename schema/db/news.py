from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from db.models.news import NewsTypeEnum
from schema.db.user import UserFields


class InlineNewsCategorySchema(BaseModel):
    category: NewsTypeEnum = Field(description="Category")


class NewsFields:
    id: int = Field()
    title: str = Field(description="Title")
    created_at: datetime = Field(description="Created at")
    categories: List[InlineNewsCategorySchema] = Field(description="Categories")


class CreateNewsSchema(BaseModel):
    title: str = NewsFields.title


class NewsSchema(BaseModel):
    id: int = NewsFields.id
    title: str = NewsFields.title
    created_at: datetime = NewsFields.created_at


class NewsWithCategoriesSchema(NewsSchema):
    categories: List[InlineNewsCategorySchema] = Field(
        description="Categories", default=[]
    )


class NewsCategorySubscribeRequestSchema(BaseModel):
    categories: List[NewsTypeEnum] = Field(description="Categories enum list")


class NewsCategorySubscribeValues(BaseModel):
    categories: List[NewsTypeEnum] = Field(description="Categories enum list")
    user_id: int = UserFields.id


class UserCategorySubscriptionSchema(BaseModel):
    category: NewsTypeEnum = Field(description="Category")
    user_id: int = UserFields.id


class UserSubscriptionNewsQuery(BaseModel):
    categories: List[NewsTypeEnum] = Field(description="Categories enum list")
    user_id: int = UserFields.id
