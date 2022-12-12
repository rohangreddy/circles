"""add content column to posts

Revision ID: fdfe9297a2c2
Revises: ad0ff94ce7a0
Create Date: 2022-12-08 16:08:08.779237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdfe9297a2c2'
down_revision = 'ad0ff94ce7a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
