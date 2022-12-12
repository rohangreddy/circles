"""add fk to posts table

Revision ID: 3023cdab8e3a
Revises: 1ec3bd0aca78
Create Date: 2022-12-08 16:20:44.639851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3023cdab8e3a'
down_revision = '1ec3bd0aca78'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", 
                           local_cols=["user_id"], remote_cols=["id"], ondelete="cascade")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
