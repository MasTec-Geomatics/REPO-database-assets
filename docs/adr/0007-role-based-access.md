# ADR 0007: Role-Based Access

- **Status:** Accepted
- **Date:** 2026-11-11

## Context

REPO data must be read-only for users and editable only by a small group of maintainers. The proof of concept serves REPO and Geomatics, but the database may later be opened to the whole company, where individual logins become hard to manage.

## Decision

Grant permissions to two group roles, never to individual people:

- `repo_reader`: read-only access.
- `repo_maintainer`: read and write access.

People get access through membership in a role.

For the proof of concept, every user gets an individual login:

```sql
CREATE ROLE jsmith LOGIN PASSWORD '...' IN ROLE repo_reader;
```

## Consequences

- Individual logins show who did what, and one person can be disabled without affecting anyone else.
- Moving to a shared reader login later is one statement, with no other changes:

  ```sql
  CREATE ROLE repo_viewer LOGIN PASSWORD '...' IN ROLE repo_reader;
  ```

- Roles belong to the whole PostgreSQL server, not one database. They are created once at server setup. Migrations grant them access inside `repo`.
- At handoff, IT chooses individual, shared, VPN-only, or company-account access. None of these require a redesign.
