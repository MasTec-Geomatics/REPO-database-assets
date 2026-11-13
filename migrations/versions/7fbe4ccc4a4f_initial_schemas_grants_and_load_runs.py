"""initial schemas, grants, and load_runs

Revision ID: 7fbe4ccc4a4f
Revises:
Create Date: 2026-11-12 14:35:52.708077

Applied migrations are never edited. To change the schema, add a new migration.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "7fbe4ccc4a4f"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# Schemas that hold REPO layers. Readers and maintainers both use these.
DATA_SCHEMAS = (
    "hydro",
    "cultural",
    "environment",
    "energy",
    "utilities",
    "land",
    "soils",
    "storage",
)

# Raw source data lands here before the swap (ADR 0005). Maintainers only: readers never see it.
STAGING_SCHEMA = "staging"


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    for schema in (*DATA_SCHEMAS, STAGING_SCHEMA):
        op.execute(f"CREATE SCHEMA {schema}")

    # Roles are created at server setup (dev/roles.sql, ADR 0007); this migration only grants.
    # ALTER DEFAULT PRIVILEGES covers tables created later by the role that runs migrations.
    for schema in DATA_SCHEMAS:
        op.execute(f"""
            GRANT USAGE ON SCHEMA {schema} TO repo_reader, repo_maintainer;

            GRANT SELECT ON ALL TABLES IN SCHEMA {schema} TO repo_reader;
            GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE
                ON ALL TABLES IN SCHEMA {schema} TO repo_maintainer;

            ALTER DEFAULT PRIVILEGES IN SCHEMA {schema}
                GRANT SELECT ON TABLES TO repo_reader;
            ALTER DEFAULT PRIVILEGES IN SCHEMA {schema}
                GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO repo_maintainer;
        """)

    # Loaders create their own staging tables with ogr2ogr, so maintainers need CREATE here.
    op.execute(f"GRANT USAGE, CREATE ON SCHEMA {STAGING_SCHEMA} TO repo_maintainer")

    op.execute("""
        CREATE TABLE public.load_runs (
            id              bigint      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            layer           text        NOT NULL,
            status          text        NOT NULL
                CONSTRAINT load_runs_status_check
                CHECK (status IN ('running', 'skipped', 'succeeded', 'failed')),
            source_version  text,
            rows_loaded     integer,
            error           text,
            started_at      timestamptz NOT NULL DEFAULT now(),
            finished_at     timestamptz
        );

        CREATE INDEX load_runs_layer_started_idx ON public.load_runs (layer, started_at);

        GRANT SELECT ON public.load_runs TO repo_reader;
        GRANT SELECT, INSERT, UPDATE ON public.load_runs TO repo_maintainer;
    """)


def downgrade() -> None:
    op.execute("DROP TABLE public.load_runs")

    # No CASCADE: if a schema still holds tables, the rollback stops instead of deleting data.
    for schema in reversed((*DATA_SCHEMAS, STAGING_SCHEMA)):
        op.execute(f"DROP SCHEMA {schema}")

    # The postgis extension is left in place. The database image installs it on its own,
    # so this migration doesn't own it.
