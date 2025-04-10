from typing import ClassVar

from pydantic import BaseModel, PositiveInt, field_validator


class ClientCommentRequestDTO(BaseModel):
    postId: PositiveInt
    id: PositiveInt
    email: str


class ServerCommentRequestDTO(ClientCommentRequestDTO):
    RESERVED_IDS: ClassVar[list[int]] = [25, 55]

    @field_validator("id")
    def id_not_reserved_validator(cls, v):
        reserved_ids = cls.RESERVED_IDS
        if v in reserved_ids:
            raise ValueError(
                f'id "{v}" are reserved. Reserved ids: {reserved_ids}'
            )
        return v

    @field_validator("id")
    def similar_symbols_validator(cls, v):
        if len(str(v)) == 3 and len(set(str(v))) == 1:
            raise ValueError(f"Id symbols can`t be the same if the length is 3")
        return v
