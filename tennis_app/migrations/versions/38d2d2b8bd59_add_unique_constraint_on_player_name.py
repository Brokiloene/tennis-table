"""add unique constraint on Player.name

Revision ID: 38d2d2b8bd59
Revises: bf655d56e134
Create Date: 2024-10-15 20:29:32.616887

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "38d2d2b8bd59"
down_revision: Union[str, None] = "bf655d56e134"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uq_player_name", "player", ["name"])


def downgrade() -> None:
    op.drop_constraint("uq_player_name", "player")
