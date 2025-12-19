"""rename risk_score to safe_score

Revision ID: 143655370e43
Revises: 46ef2cade112
Create Date: 2025-12-19 20:52:22.163220

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "143655370e43"
down_revision: Union[str, None] = "46ef2cade112"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename column risk_score to safe_score (preserves data)
    with op.batch_alter_table("trade_safety_checks", schema=None) as batch_op:
        batch_op.alter_column("risk_score", new_column_name="safe_score")


def downgrade() -> None:
    # Rename column safe_score back to risk_score
    with op.batch_alter_table("trade_safety_checks", schema=None) as batch_op:
        batch_op.alter_column("safe_score", new_column_name="risk_score")
