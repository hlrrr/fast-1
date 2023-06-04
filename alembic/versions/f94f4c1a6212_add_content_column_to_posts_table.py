"""add, content column to posts table

Revision ID: f94f4c1a6212
Revises: abd0cf10923a
Create Date: 2023-06-04 15:11:34.457228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f94f4c1a6212'
down_revision = 'abd0cf10923a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('content', sa.String(), nullable=False)
                  )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
