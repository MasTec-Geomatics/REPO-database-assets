# ADR 0004: Store All Geometry in WGS84 (EPSG:4326)

- **Status:** Accepted
- **Date:** 2026-11-11

## Context

Source data arrives in several coordinate systems (NAD83, NAD27, others). Texas spans several State Plane zones, and the database is planned to expand to the continental United States.

## Decision

Store every geometry column in WGS84 (`EPSG:4326`). Loaders reproject on load with `ogr2ogr -t_srs EPSG:4326`.

## Consequences

- One coordinate system across all layers and all future states.
- No separate transformation scripts; reprojection happens during loading.
- NAD83(2011) and WGS84 differ by up to one to two meters within the continental United States. This is acceptable for risk screening.
- Distances and areas are not meaningful in degrees. Measurements use the PostGIS `geography` type or reproject inside the query.
- QGIS reprojects on the fly, so users can still work in State Plane in their own projects.
