# ADR 0001: Separate `repo` Database on the Atlas PostgreSQL Server

- **Status:** Accepted
- **Date:** 2026-11-11

## Context

REPO needs a shared, read-only GIS reference database. Project Atlas already runs a PostgreSQL/PostGIS server for Geomatics project data.

The two datasets behave differently:

- **Atlas** holds working data that users edit daily.
- **REPO** holds public reference data that scripts replace in bulk on a schedule.

REPO may later be opened to the whole company and handed to IT to host.

## Decision

Create a separate database named `repo` on the same PostgreSQL server that hosts `atlas`.

## Consequences

- One server to run and maintain.
- Bulk REPO loads cannot interfere with Atlas data.
- Permissions stay simple: REPO users are granted access to `repo` only and never see `atlas`.
- Each database is backed up and restored on its own.
- IT can move `repo` to its own server at handoff without touching Atlas.
- A single SQL query cannot join tables across the two databases. If Atlas needs REPO data, the `postgres_fdw` extension can expose REPO tables inside Atlas.
- QGIS users who use both need two connections: same host and port, different database name.
