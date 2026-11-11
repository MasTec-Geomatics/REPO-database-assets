# ADR 0003: Alembic with Raw SQL for Migrations

- **Status:** Accepted
- **Date:** 2026-11-11

## Context

The `repo` database needs versioned schema changes: the PostGIS extension, schemas, roles and grants, and table definitions.

Options considered:

- **goose with plain `.sql` files.** Matches the lead maintainer's Go projects, but adds a Go tool to a Python project.
- **Alembic with `.sql` files referenced from each migration.** Real SQL files, but a custom folder convention every maintainer must learn.
- **Alembic with SQL inside each migration.** The standard Python tool, used as-is.

The other maintainers and IT know Python, not Go.

## Decision

Use Alembic. Each migration contains raw SQL through `op.execute()`. No ORM models.

## Consequences

- One language and one toolchain in the project.
- Any Python developer who knows Alembic can maintain it without learning a custom convention.
- SQL lives inside Python strings, so editors don't provide SQL highlighting or checking for it.
- Migrations are run with `alembic upgrade head` before loaders run: on deploy for a Droplet, or as a one-time Job on Kubernetes.
- Applied migrations are never edited. Changes are made with new migrations.
