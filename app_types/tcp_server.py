from pydantic import BaseModel, PositiveInt, validator, field_validator


class ClientCommentRequestDTO(BaseModel):
    postId: PositiveInt
    id: PositiveInt
    email: str


class ServerCommentRequestDTO(ClientCommentRequestDTO):

    @field_validator("id")
    def id_validator(cls, v):
        reserved_ids = [25, 55]
        if v in reserved_ids:
            raise ValueError(f"id \"{v}\" are reserved. Reserved ids: {reserved_ids}")
        if len(str(v)) == 3 and len(set(str(v))) == 1:
            raise ValueError(f"Id symbols can`t be the same if the length is 3")
        return v
