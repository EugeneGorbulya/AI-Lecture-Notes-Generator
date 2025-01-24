"""Add type column to messages

Revision ID: a36295471087
Revises: d1f5edd21a58
Create Date: 2025-01-24 15:07:22.688072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a36295471087'
down_revision: Union[str, None] = 'd1f5edd21a58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем столбец без ограничения NOT NULL
    op.add_column(
        'messages',
        sa.Column('type', sa.Enum('TEXT', 'VIDEO', 'FILE', name='messagetype'), nullable=True)
    )

    # Присваиваем значение по умолчанию для существующих строк
    op.execute("UPDATE messages SET type = 'TEXT'")

    # Меняем столбец, чтобы сделать его NOT NULL
    op.alter_column(
        'messages',
        'type',
        nullable=False,
        existing_type=sa.Enum('TEXT', 'VIDEO', 'FILE', name='messagetype')
    )

def downgrade() -> None:
    # Удаляем столбец
    op.drop_column('messages', 'type')

