"""Add description field

Revision ID: 20f90e162aba
Revises: e951180bbd82
Create Date: 2024-09-28 09:44:15.108142

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20f90e162aba"
down_revision: Union[str, None] = "e951180bbd82"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Добавление колонки description в таблицу videos
    op.add_column("videos", sa.Column("description", sa.String(), nullable=True))


def downgrade():
    # Удаление колонки description из таблицы videos
    op.drop_column("videos", "description")
