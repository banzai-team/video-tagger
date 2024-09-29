"""add another text field

Revision ID: a09f00cec53c
Revises: 45bc42eebb9a
Create Date: 2024-09-29 08:09:20.912163

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a09f00cec53c"
down_revision: Union[str, None] = "45bc42eebb9a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("videos", sa.Column("frames_text", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("videos", "frames_text")
