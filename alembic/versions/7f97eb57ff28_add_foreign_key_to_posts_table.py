"""Add foreign key to posts table

Revision ID: 7f97eb57ff28
Revises: 3b471d9a4bf4
Create Date: 2025-03-14 08:10:35.221781

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import INTEGER, Column, ForeignKey


# revision identifiers, used by Alembic.
revision: str = '7f97eb57ff28'
down_revision: Union[str, None] = '3b471d9a4bf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", Column("owner_id", INTEGER, nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
