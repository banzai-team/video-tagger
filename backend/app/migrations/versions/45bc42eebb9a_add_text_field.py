"""Add text field

Revision ID: 45bc42eebb9a
Revises: 20f90e162aba
Create Date: 2024-09-28 14:59:17.524269

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "45bc42eebb9a"
down_revision: Union[str, None] = "20f90e162aba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Добавление колонки description в таблицу videos
    op.add_column("videos", sa.Column("text", sa.String(), nullable=True))
    op.add_column("videos", sa.Column("audio_path", sa.String(), nullable=True))
    op.add_column("videos", sa.Column("tags", sa.String(), nullable=True))
    op.alter_column("videos", "file_path", new_column_name="video_path")


def downgrade():
    # Удаление колонки description из таблицы videos
    op.alter_column("videos", "video_path", new_column_name="file_path")
    op.drop_column("videos", "text")
    op.drop_column("videos", "tags")
    op.drop_column("videos", "audio_path")
