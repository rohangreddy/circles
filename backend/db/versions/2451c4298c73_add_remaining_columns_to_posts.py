"""add remaining columns to posts

Revision ID: 2451c4298c73
Revises: 3023cdab8e3a
Create Date: 2022-12-08 16:26:08.108481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2451c4298c73'
down_revision = '3023cdab8e3a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
