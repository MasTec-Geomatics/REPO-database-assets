"""Alembic environment for the REPO database.

Migrations are raw SQL through op.execute(). There are no ORM models and no autogenerate.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool
from sqlalchemy.engine import URL, make_url

from repo_loaders.config import ConfigError, load_settings

CONNECT_TIMEOUT_SECONDS = 10

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def database_url() -> URL:
    try:
        url = load_settings().database_url
    except ConfigError as exc:
        raise SystemExit(
            f"Cannot run migrations: {exc}. Set it in .env or the environment."
        ) from exc

    # REPO_DATABASE_URL is a plain postgresql:// URL. SQLAlchemy needs to be told to use psycopg 3.
    return make_url(url).set(drivername="postgresql+psycopg")


def run_migrations_offline() -> None:
    """Write the migration SQL to stdout instead of runniing it (`alembic upgrade head --sql`)."""
    context.configure(url=database_url(), literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(
        database_url(),
        poolclass=pool.NullPool,
        connect_args={
            "connect_timeout": CONNECT_TIMEOUT_SECONDS,
            "application_name": "repo-migrations",
        },
    )
    with engine.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
