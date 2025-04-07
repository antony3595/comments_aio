from sqlalchemy import Column, String, VARCHAR, DateTime
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class AuthUser(BaseModel):
    __tablename__ = 'auth_users'

    email = Column(VARCHAR(255), unique=True, nullable=False)
    full_name = Column(VARCHAR(255), nullable=False)


class ServiceAccount(BaseModel):
    __tablename__ = 'service_accounts'
    name = Column(VARCHAR(255), unique=True, nullable=False)
    token = Column(VARCHAR(255), nullable=False)
    token_valid_date = Column(DateTime, nullable=False)
    raw_news = relationship("RawNews", back_populates="service_account")
