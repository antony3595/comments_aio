from fake_db.db import USERS_TABLE
from repository.base import BaseRepository
from schema.db.user import UserSchema
from schema.query.user import UserEmailQuery


class UserRepository(BaseRepository):
    def read(self, query: UserEmailQuery) -> UserSchema | None:
        for user in USERS_TABLE:
            if query.email == user.get("email"):
                return UserSchema(**user)
        return None

    def create(self, query: UserSchema):
        USERS_TABLE.append(query.model_dump())
        return query
