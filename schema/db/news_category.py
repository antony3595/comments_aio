from typing import List

from pydantic import BaseModel, Field

from db.models.news import NewsTypeEnum
from schema.db.news import NewsFields


class NewsCategorySchema(BaseModel):
    id: int = Field(description="ID")
    category: NewsTypeEnum = Field(description="Category")


class CreateNewsCategoriesSchema(BaseModel):
    news_id: int = NewsFields.id
    categories: List[NewsTypeEnum] = Field(
        description="Categories list", examples=[e.value for e in NewsTypeEnum]
    )
