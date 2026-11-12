"""Database connections."""

import psycopg
from psycopg.rows import TupleRow

CONNECT_TIMEOUT_SECONDS = 10


def connect(database_url: str) -> psycopg.Connection[TupleRow]:
    return psycopg.connect(
        database_url,
        connect_timeout=CONNECT_TIMEOUT_SECONDS,
        application_name="repo-loaders",
    )
