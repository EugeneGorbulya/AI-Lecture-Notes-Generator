"""update

Revision ID: d1f5edd21a58
Revises: f669bc052ea4
Create Date: 2025-01-24 14:53:00.812180

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision = "d1f5edd21a58"  # Убедитесь, что это строка, а не тип `str`
down_revision = "f669bc052ea4"  # ID предыдущей миграции
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TYPE messagetype ADD VALUE 'video'")
    # ### end Alembic commands ###


def downgrade() -> None:
    # Откат значений в ENUM невозможно автоматизировать.
    pass
