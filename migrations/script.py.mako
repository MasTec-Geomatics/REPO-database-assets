"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

Applied migrations are never edited. To change the schema, add a new migration.
"""
from collections.abc import Sequence

from alembic import op

revision: str = ${repr(up_revision)}
down_revision: str | Sequence[str] | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}

def upgrade() -> None:
    op.execute("""
    """)

def downgrade() -> None:
    op.execute("""
    """)
