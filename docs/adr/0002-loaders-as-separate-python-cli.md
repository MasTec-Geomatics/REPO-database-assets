# ADR 0002: Loaders as a Separate Repository and Plain Python CLI

- **Status:** Accepted
- **Date:** 2026-11-11

## Context

Each REPO layer needs a job that downloads public data and loads it into the `repo` database on a schedule.

These jobs could live inside the Atlas FastAPI application or in their own project. REPO is expected to be handed to IT, and the other maintainers and IT know Python.

## Decision

The loaders live in their own repository as a plain Python command-line program. There is no web framework.

- One command per layer, e.g. `repo-load wetlands`.
- Each run does one job, exits with a status code, and logs what happened.
- `argparse` for the command line, `httpx` for downloads, GDAL's `ogr2ogr` for loading GIS data, `psycopg` for the loader's own SQL, and `structlog` for logging.
- One module per layer under `layers/`.

## Consequences

- REPO is self-contained: the database plus its loaders. IT can take it over without running Atlas.
- Python matches the skills of the other maintainers and IT.
- The scheduler only runs a command. Moving from systemd timers to Kubernetes CronJobs does not change any loader code.
- The container image must include GDAL, since `ogr2ogr` does the GIS loading.
