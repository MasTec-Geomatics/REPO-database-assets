# ADR 0006: Elevation Rasters in AWS S3, Not PostGIS

- **Status:** Accepted
- **Date:** 2026-11-11

## Context

Topography comes from USGS 3DEP 1-meter digital elevation models (DEMs). These are rasters (grids of cells), not points, lines, or polygons.

Texas covers about 268,000 square miles. At 1-meter resolution, that is roughly 690 billion cells, on the order of 2.8 TB uncompressed.

## Decision

Store DEM tiles as Cloud Optimized GeoTIFFs (COGs) in AWS S3, plus one mosaic file (`dem_1m/tx/texas_dem.vrt`) that references every tile.

Record each file in the `storage.raster_assets` table with its S3 key, URL, source, source date, and footprint polygon.

## Consequences

- The database stays small, so backups, restores, and the server itself stay fast.
- Object storage costs less per gigabyte than database storage.
- QGIS streams only the part of a COG that is on screen. Users never download the full dataset.
- Users can see tile coverage in QGIS by adding `storage.raster_assets`.
- QGIS users need read-only AWS credentials, set once in QGIS's own environment settings. No admin rights are needed.
- Raster data is not queryable with SQL inside the database.
