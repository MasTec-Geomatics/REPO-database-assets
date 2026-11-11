# ADR 0005: Two-Step Loads with a Weekly Change Check

- **Status:** Accepted
- **Date:** 2026-11-11

## Context

Public sources change on different schedules, and agencies can rename or restructure their fields without notice. REPO users must never see a half-loaded layer.

## Decision

Every loader follows the same process:

1. **Check.** Weekly, compare the source's `Last-Modified`, `ETag`, or published release date with the last successful run in `public.load_runs`. If nothing changed, record the run as `skipped` and exit.
2. **Stage.** Load the raw source into a `staging` schema as-is with `ogr2ogr`.
3. **Swap.** In one transaction, empty the final table and insert the mapped columns from staging.

Final tables are defined in migrations, not created by the loader.

## Consequences

- Column names stay stable even when a source renames fields, so QGIS styles and saved queries keep working.
- When a source changes its structure, the loader fails loudly instead of silently changing the table.
- Users keep seeing the previous data until the swap transaction commits.
- Each layer needs a column mapping written once, when its loader is built.
- Every run is recorded in `public.load_runs` with its status, row count, and source version.
- The weekly schedule can be adjusted per layer later.
