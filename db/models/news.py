from sqlalchemy import Column, VARCHAR

from db.models.base import BaseModel


class News(BaseModel):
    __tablename__ = 'news'
    title = Column(VARCHAR(255), nullable=False)
