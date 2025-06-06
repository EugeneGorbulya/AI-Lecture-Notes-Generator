"""add sender to messages

Revision ID: bf754dde684d
Revises: a36295471087
Create Date: 2025-05-25 15:59:43.735194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf754dde684d'
down_revision: Union[str, None] = 'a36295471087'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'messages',
        sa.Column('sender', sa.String(), nullable=False, server_default='user')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'sender')
    # ### end Alembic commands ###
