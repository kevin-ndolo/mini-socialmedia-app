"""Add user table

Revision ID: 3b471d9a4bf4
Revises: f987268b7b43
Create Date: 2025-03-14 08:00:43.749946

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import INTEGER, TIMESTAMP, Column, String, func, PrimaryKeyConstraint, UniqueConstraint


# revision identifiers, used by Alembic.
revision: str = '3b471d9a4bf4'
down_revision: Union[str, None] = 'f987268b7b43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                     Column("id", INTEGER, nullable=False),
                     Column("email", String(), nullable=False),
                     Column("password", String(), nullable=False),
                     Column("created_at",  TIMESTAMP(timezone=True), server_default=func.now(), nullable=False),
                     PrimaryKeyConstraint("id"),
                     UniqueConstraint("email")
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
