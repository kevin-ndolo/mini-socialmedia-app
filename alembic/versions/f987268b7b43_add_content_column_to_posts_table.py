""" add content column to posts table

Revision ID: f987268b7b43
Revises: 91c5c1da8090
Create Date: 2025-03-14 07:17:05.378530

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column, String


# revision identifiers, used by Alembic.
revision: str = 'f987268b7b43'
down_revision: Union[str, None] = '91c5c1da8090'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", Column("content", String(), nullable=False ))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
