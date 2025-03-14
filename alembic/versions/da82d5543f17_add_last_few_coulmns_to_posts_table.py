"""Add last few coulmns to posts table

Revision ID: da82d5543f17
Revises: 7f97eb57ff28
Create Date: 2025-03-14 08:18:08.143606

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import TIMESTAMP, Boolean, Column, String, func


# revision identifiers, used by Alembic.
revision: str = 'da82d5543f17'
down_revision: Union[str, None] = '7f97eb57ff28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", Column("published", Boolean(), nullable=False , server_default="TRUE"))
    Column("created_at",  TIMESTAMP(timezone=True), server_default=func.now(), nullable=False),
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
