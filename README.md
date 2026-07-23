# pluginlake-ehds-demo

An [EHDS](https://health.ec.europa.eu/ehealth-digital-health-and-care/european-health-data-space-ehds_en)
demo [pluginlake](https://github.com/plugin-healthcare/pluginlake) project package.

It plugs into a pluginlake node through a single `ProjectManifest`
(`src/ehds_demo/manifest.py`) and owns the `ducklake` DuckLake catalog and the
`ehds-demo` asset-URN namespace (ADR-009). Core discovers it via the
`pluginlake.projects` entry point and mounts its contributions uniformly.

## What it contributes

- **Dagster code locations:** `ehds_demo.definitions.omop`, `ehds_demo.definitions.fhir`.
- **Toolkits:** `ehds_demo.omop` (OMOP CDM load/validate/query) and
  `ehds_demo.fhir` (FHIR R4 load + plugin-rosetta translation to OMOP).
- **API routers:** OMOP/FHIR upload and statistics endpoints, mounted by the core
  gateway within the project namespace and behind its authn/authz scope.

> The OMOP/FHIR routers are carried as bespoke routers for now. In the target
> model (ADR-009) statistics become registered predefined queries and uploads
> ride the generic `/api/v1/ingest` endpoint; the routers will be retired once
> that mechanism lands.

## Develop

```bash
uv sync
uv run pluginlake verify   # conformance check against the plugin contract
uv run pytest
```

`pluginlake` (core) is co-developed from the sibling `../pluginlake` checkout
(see `[tool.uv.sources]`). The `plugin-rosetta` FHIR translation engine is
pinned to the same revision core uses.
