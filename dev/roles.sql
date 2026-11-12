-- Group roles for REPO access (ADR 0007).
-- Roles belong to the whole server ,so they're created at server setup, not in migrations.
-- Safe to run more than once.

DO $$
  BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'repo_reader') THEN
      CREATE ROLE repo_reader NOLOGIN;
    END IF;

    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'repo_maintainer') THEN
      CREATE ROLE repo_maintainer NOLOGIN;
    END IF;
  END
$$;

-- Maintainers can do everything readers can.
GRANT repo_reader TO repo_maintainer;
