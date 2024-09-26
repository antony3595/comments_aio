from pydantic import Field, BaseModel


class PaginationSchema(BaseModel):
    page: int = Field(default=1)
    size: int = Field(default=10)
