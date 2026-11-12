# Local development database (podman). Run `just` to list recipes.

pod_file := "dev/repo-db.yaml"
container := "repo-db-postgis"
volume := "repo-db-data"

# List recipes
default:
  @just --list

# Start the local PostGIS pod
db-up:
  podman kube play {{pod_file}}

# Stop and remove the pod (data in the volume is kept)
db-down:
  podman kube down {{pod_file}}

# Delete the pod AND its data, then start fresh
[confirm("This deletes all local REPO database data. Continue?")]
db-reset:
  -podman kube down {{pod_file}}
  -podman volume rm {{volume}}
  podman kube play {{pod_file}}

# Follow the database logs
db-logs:
  podman logs -f {{container}}

# Open psql inside the container
db-psql:
  podman exec -it {{container}} psql -U repo -d repo

# Connect through the app's own code (checks .env and the password)
db-check:
  uv run python -c "from repo_loaders.config import load_settings; from repo_loaders.db import connect; c = connect(load_settings().database_url); print(c.execute('SELECT postgis_full_version()').fetchone()); c.close()"

# Create the repo_reader and repo_maintainer group roles (safe to re-run)
db-roles:
  podman exec -i {{container}} psql -U repo -d repo -v ON_ERROR_STOP=1 < dev/roles.sql

# Apply all migrations
db-migrate:
  uv run alembic upgrade head

# Create a new migration: just db-revision "create hydro schema"
db-revision message:
  uv run alembic revision -m "{{message}}"


