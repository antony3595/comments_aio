import enum

from sqlalchemy import Column, VARCHAR, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class NewsTypeEnum(enum.Enum):
    WORLD_EVENTS = "Мировые события"
    POLITICS = "Политика"
    ECONOMY = "Экономика"
    SCIENCE_AND_TECHNOLOGY = "Наука и технологии"
    HEALTHCARE = "Здравоохранение"
    ENVIRONMENT = "Экология"
    CULTURE_AND_ARTS = "Культура и искусство"
    SPORTS = "Спорт"
    SOCIETY = "Общество"
    ENTERTAINMENT = "Развлечения"


class News(BaseModel):
    __tablename__ = 'news'
    title = Column(VARCHAR(255), nullable=False)
    categories = relationship("NewsCategory", back_populates="news")


class NewsCategory(BaseModel):
    __tablename__ = 'news_categories'
    category = Column(Enum(NewsTypeEnum), nullable=False)
    news_id = Column(ForeignKey("news.id"), nullable=False)
    news = relationship("News", back_populates="categories")

    __table_args__ = (UniqueConstraint(category, news_id),)


class UserCategorySubscription(BaseModel):
    __tablename__ = 'users_categories_subscriptions'
    category = Column(Enum(NewsTypeEnum), nullable=False)
    user_id = Column(ForeignKey("auth_users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("AuthUser", backref="categories")

    __table_args__ = (UniqueConstraint(category, user_id),)
