from sqlalchemy import Column, String, VARCHAR

from db.models.base import BaseModel


class AuthUser(BaseModel):
    __tablename__ = 'auth_users'

    email = Column(VARCHAR(255), unique=True, nullable=False)
    full_name = Column(VARCHAR(255), nullable=False)
