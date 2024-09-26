import enum

from sqlalchemy import Column, VARCHAR, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class NewsTypeEnum(enum.Enum):
    WORLD_EVENTS = "WORLD_EVENTS"
    POLITICS = "POLITICS"
    ECONOMY = "ECONOMY"
    SCIENCE_AND_TECHNOLOGY = "SCIENCE_AND_TECHNOLOGY"
    HEALTHCARE = "HEALTHCARE"
    ENVIRONMENT = "ENVIRONMENT"
    CULTURE_AND_ARTS = "CULTURE_AND_ARTS"
    SPORTS = "SPORTS"
    SOCIETY = "SOCIETY"
    ENTERTAINMENT = "ENTERTAINMENT"


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
