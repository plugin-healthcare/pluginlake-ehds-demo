# pluginlake-ehds-demo

An [EHDS](https://health.ec.europa.eu/ehealth-digital-health-and-care/european-health-data-space-ehds_en)
demo [pluginlake](https://github.com/plugin-healthcare/pluginlake) project package.

It plugs into a pluginlake node through a single `ProjectManifest`
(`src/ehds_demo/manifest.py`) and owns the `ducklake` DuckLake catalog and the
`ehds-demo` asset-URN namespace (ADR-009). Core discovers it via the
`pluginlake.projects` entry point and mounts its contributions uniformly. For
how projects are onboarded and deployed onto a station, see the core
[Deploying a Station](https://github.com/plugin-healthcare/pluginlake) guide.

## What it contributes

- **Dagster code locations:** `ehds_demo.definitions.omop`, `ehds_demo.definitions.fhir`.
- **Toolkits:** [`ehds_demo.omop`](reference/omop.md) (OMOP CDM load, validate, query) and
  [`ehds_demo.fhir`](reference/fhir.md) (FHIR R4 load and plugin-rosetta translation to OMOP).
- **API routers:** OMOP and FHIR upload and statistics endpoints, mounted by the core
  gateway within the project namespace.

## Reference

- [OMOP](reference/omop.md) — the OMOP CDM toolkit.
- [FHIR](reference/fhir.md) — the FHIR loading and translation toolkit.
