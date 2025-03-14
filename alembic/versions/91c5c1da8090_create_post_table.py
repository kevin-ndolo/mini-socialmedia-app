"""Create post table

Revision ID: 91c5c1da8090
Revises: 
Create Date: 2025-03-14 07:02:12.060476

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column, String


# revision identifiers, used by Alembic.
revision: str = '91c5c1da8090'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.create_table(
        "posts",
        Column("id", INTEGER, primary_key=True, nullable=False),
        Column("title", String(), nullable=False),
    
    )

    pass
    


def downgrade() -> None:
    op.drop_table("posts")
    pass
