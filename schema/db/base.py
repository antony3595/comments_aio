from typing import Dict, Any, ClassVar

from pydantic import Field, BaseModel

from db.models.base import BaseModel as BaseOrmModel
from services.common.exceptions import BaseSchemaException


class BaseSchema(BaseModel):
    model: ClassVar[type[BaseOrmModel] | None] = None

    def to_orm_filters(self, raise_on_wrong_attribute=True) -> Dict[str, Any]:
        """Works only for equal cases for now"""
        assert (
            self.model is not None
        ), f'{self.__class__.__name__} must have a "model" attribute to compute filters'

        filters = {}
        for field, value in self.model_dump(exclude_unset=True).items():
            if hasattr(self.model, field):
                filters[field] = value
            elif raise_on_wrong_attribute:
                raise BaseSchemaException(
                    f"{self.__class__.__name__} field {field} is not defined"
                )
        return filters


class PaginationSchema(BaseModel):
    page: int = Field(default=1)
    size: int = Field(default=10)
