"""Add username to users table

Revision ID: 3f11fa71b932
Revises: 
Create Date: 2025-01-24 10:27:26.795485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3f11fa71b932'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Commands to add the username column
    op.add_column(
        'users',
        sa.Column('username', sa.String(length=255), nullable=False)
    )

    # Optionally, if you want to add a unique constraint or index:
    op.create_unique_constraint('uq_users_username', 'users', ['username'])


def downgrade():
    # Commands to remove the username column
    op.drop_constraint('uq_users_username', 'users', type_='unique')
    op.drop_column('users', 'username')