# ADR 0008: QGIS Connects Directly to PostgreSQL over TLS

- **Status:** Accepted
- **Date:** 2026-11-11

## Context

The team is remote and works on locked-down company laptops that cannot install VPN clients. QGIS is the team's GIS program.

A test from a standard work laptop (`Test-NetConnection hh-pgsql-public.ebi.ac.uk -Port 5432`) confirmed that outbound traffic on port `5432` is allowed.

## Decision

QGIS connects directly to PostgreSQL on port `5432`, encrypted with TLS (`SSL mode = verify-full`). There is no web service layer between QGIS and the database.

## Consequences

- Nothing to build or run between users and the data.
- Each user sets up one PostgreSQL connection in QGIS.
- Shared layer styles are stored in `public.layer_styles` and load with each layer.
- The database port is reachable from the internet. TLS and individual logins protect it.
- If a future network change blocks port `5432`, the fallback is to serve layers read-only over HTTPS through a standard OGC web service.
