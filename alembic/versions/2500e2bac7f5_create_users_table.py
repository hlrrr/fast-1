"""create, Users table

Revision ID: 2500e2bac7f5
Revises: f94f4c1a6212
Create Date: 2023-06-04 15:21:58.799924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2500e2bac7f5'
down_revision = 'f94f4c1a6212'
branch_labels = None
depends_on = None


def upgrade() -> None:
        op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),      # Or Column option 
                    sa.UniqueConstraint('email')        # Or Column option
                    )


def downgrade() -> None:
    pass
