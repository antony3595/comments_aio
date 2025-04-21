"""raw_news

Revision ID: 2dd3c4242960
Revises: 4bda85823d17
Create Date: 2024-09-29 20:24:31.203997

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "2dd3c4242960"
down_revision: Union[str, None] = "4bda85823d17"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "service_accounts",
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("token", sa.VARCHAR(length=255), nullable=False),
        sa.Column("token_valid_date", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "raw_news",
        sa.Column(
            "data", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("processed", sa.Boolean(), nullable=False),
        sa.Column("service_account_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["service_account_id"], ["service_accounts.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("raw_news")
    op.drop_table("service_accounts")
