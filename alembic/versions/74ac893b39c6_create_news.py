"""create news

Revision ID: 74ac893b39c6
Revises: 945ade7b1794
Create Date: 2024-08-24 22:56:22.251887

"""
from typing import Sequence, Union

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from alembic import op
from db.models.news import News

# revision identifiers, used by Alembic.
revision: str = '74ac893b39c6'
down_revision: Union[str, None] = '945ade7b1794'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


async def create_news(db: AsyncSession) -> None:
    await db.execute(
        insert(News),
        [{"title": "Defenseless"},
         {"title": "Eye for an Eye, An"},
         {"title": "Corto Maltese: Under the Sign of Capricorn (Sous le signe du capricorne)"},
         {"title": "Down in the Delta"},
         {"title": "Dr. Dolittle 3"},
         {"title": "Noises Off..."},
         {"title": "Metroland"},
         {"title": "Vatel"},
         {"title": "McConkey"},
         {"title": "Before Flying Back to Earth (Pries parskrendant i zeme)"}]
    )


def upgrade() -> None:
    op.run_async(create_news)


def downgrade() -> None:
    pass
