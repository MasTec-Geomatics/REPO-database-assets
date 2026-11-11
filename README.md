# REPO GIS Database

![Status](https://img.shields.io/badge/status-proof%20of%20concept-orange)
![Phase](https://img.shields.io/badge/phase%201-Texas-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![PostGIS](https://img.shields.io/badge/PostGIS-336791)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-D71F00?logo=sqlalchemy&logoColor=white)
![GDAL](https://img.shields.io/badge/GDAL-5CAE58?logo=gdal&logoColor=white)
![QGIS](https://img.shields.io/badge/QGIS-589632?logo=qgis&logoColor=white)
![DigitalOcean](https://img.shields.io/badge/DigitalOcean-0080FF?logo=digitalocean&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS%20S3-569A31)

A shared, read-only GIS reference database for the REPO group (Business Development & Estimating). It gives estimators project-risk data from public sources when an owner or client has not provided it.

Phase 1 covers Texas. All data is viewed in QGIS.

## How It Works

| Part | What it does |
| --- | --- |
| **Database** | `repo` database on the Atlas PostgreSQL/PostGIS server. All geometry in WGS84 (`EPSG:4326`). |
| **Loaders** | Python CLI, one command per layer. Checks each source weekly and reloads only when the source changed. |
| **Raster storage** | 1-meter elevation models stored in AWS S3 as Cloud Optimized GeoTIFFs, tracked in `storage.raster_assets`. |
| **Access** | Read-only for REPO users through `repo_reader`; edits only through `repo_maintainer`. |
| **QGIS** | Direct PostgreSQL connection on port `5432` over TLS. Elevation data streams from S3. |

## Layers

| Schema | Table | Source |
| --- | --- | --- |
| `hydro` | `wetlands` | USFWS National Wetlands Inventory |
| `hydro` | `flowlines`, `waterbodies` | USGS 3D Hydrography Program |
| `hydro` | `stream_segments` | TCEQ |
| `hydro` | `flood_fema` | FEMA National Flood Hazard Layer |
| `hydro` | `flood_ble` | TWDB Base Level Engineering |
| `cultural` | `nrhp` | National Park Service |
| `cultural` | `cemeteries`, `markers` | Texas Historical Commission |
| `environment` | `critical_habitat` | USFWS ECOS |
| `energy` | `oilgas_wells`, `pipelines` | Railroad Commission of Texas |
| `utilities` | `water_wells` | TWDB Groundwater Database |
| `land` | `protected_areas` | USGS PAD-US 4.1 |
| `land` | `parcels` | TxGIO StratMap Land Parcels |
| `soils` | `map_units` | USDA NRCS gSSURGO |
| `storage` | `raster_assets` | USGS 3DEP 1-meter DEM (files in S3) |
| `public` | `load_runs` | Load history |

### Not Publicly Available

Archaeological sites, Texas rare species (TXNDD), electric transmission lines, federal pipelines (NPMS), TxDOT right-of-way, local utilities, and tile drain.

## Repository Contents

```text
.
├── docs/
│   ├── adr/            Architecture decision records
│   └── repo-db.dbml    Database schema (paste into dbdiagram.io for the ERD)
└── README.md
```

## Architecture Decisions

| ADR | Decision |
| --- | --- |
| [0001](docs/adr/0001-separate-repo-database-on-atlas-server.md) | Separate `repo` database on the Atlas PostgreSQL server |
| [0002](docs/adr/0002-loaders-as-separate-python-cli.md) | Loaders as a separate repository and plain Python CLI |
| [0003](docs/adr/0003-alembic-with-raw-sql-migrations.md) | Alembic with raw SQL for migrations |
| [0004](docs/adr/0004-store-geometry-in-wgs84.md) | Store all geometry in WGS84 (`EPSG:4326`) |
| [0005](docs/adr/0005-two-step-loads-with-weekly-change-check.md) | Two-step loads with a weekly change check |
| [0006](docs/adr/0006-elevation-rasters-in-s3.md) | Elevation rasters in AWS S3, not PostGIS |
| [0007](docs/adr/0007-role-based-access.md) | Role-based access |
| [0008](docs/adr/0008-qgis-direct-postgresql-connection.md) | QGIS connects directly to PostgreSQL over TLS |

## Connecting from QGIS

**Database layers**

```text
QGIS → Browser panel → right-click "PostgreSQL" → New Connection

  Name:      REPO
  Host:      <server address>
  Port:      5432
  Database:  repo
  SSL mode:  verify-full
  Auth:      your own login
```

**Elevation (S3)**

```text
QGIS → Settings → Options → System → Environment → Use custom variables

  AWS_ACCESS_KEY_ID      = <read-only key>
  AWS_SECRET_ACCESS_KEY  = <read-only secret>
  AWS_DEFAULT_REGION     = <bucket region>

Restart QGIS, then:

QGIS → Layer → Data Source Manager → Raster

  Source type:  Protocol: HTTP(S), cloud, etc.
  Type:         AWS S3
  Bucket:       <repo bucket name>
  Object key:   dem_1m/tx/texas_dem.vrt
```
