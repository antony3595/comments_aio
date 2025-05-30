import enum

from sqlalchemy import (
    Column,
    VARCHAR,
    ForeignKey,
    UniqueConstraint,
    Enum,
    Boolean,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, mapped_column

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
    __tablename__ = "news"
    title = Column(VARCHAR(255), nullable=False)
    categories = relationship("NewsCategory", back_populates="news")


class NewsCategory(BaseModel):
    __tablename__ = "news_categories"
    category = mapped_column(Enum(NewsTypeEnum), nullable=False)
    news_id = mapped_column(ForeignKey("news.id"), nullable=False)
    news = relationship("News", back_populates="categories")

    __table_args__ = (UniqueConstraint(category, news_id),)


class UserCategorySubscription(BaseModel):
    __tablename__ = "users_categories_subscriptions"
    category = mapped_column(Enum(NewsTypeEnum), nullable=False)
    user_id = mapped_column(
        ForeignKey("auth_users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("AuthUser", backref="categories")

    __table_args__ = (UniqueConstraint(category, user_id),)


class RawNews(BaseModel):
    __tablename__ = "raw_news"
    data = Column(JSONB, nullable=False)
    processed = Column(Boolean, nullable=False, default=False)
    service_account_id = mapped_column(
        ForeignKey("service_accounts.id", ondelete="CASCADE"), nullable=False
    )
    service_account = relationship("ServiceAccount", back_populates="raw_news")
