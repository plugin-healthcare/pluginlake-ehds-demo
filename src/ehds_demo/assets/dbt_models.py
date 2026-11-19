"""Dagster-managed dbt models for the local DuckLake demo."""

import json
from collections.abc import Iterator
from pathlib import Path
from tempfile import TemporaryDirectory

from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from dagster_dbt.core.dbt_event_iterator import DbtDagsterEventType
from pluginlake.core.config import DuckLakeSettings

PROJECT = Path(__file__).resolve().parents[1] / "dbt"


def _dbt(workdir: Path, attachment: dict | None = None) -> DbtCliResource:
    target = {"type": "duckdb", "path": str(workdir / "ducklake.duckdb"), "schema": "ehds_demo", "threads": 1}
    if attachment:
        target.update(path=str(workdir / "session.duckdb"), database="ducklake", attach=[attachment])
    profile = {"ehds_demo": {"target": "demo", "outputs": {"demo": target}}}
    (workdir / "profiles.yml").write_text(json.dumps(profile))
    return DbtCliResource(project_dir=str(PROJECT), profiles_dir=str(workdir))


def _manifest() -> dict:
    """Parse the packaged model without opening the station catalog during code discovery."""
    with TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        invocation = _dbt(workdir).cli(["parse"], target_path=workdir / "target").wait()
        return invocation.get_artifact("manifest.json")


@dbt_assets(manifest=_manifest(), name="ehds_demo_dbt_models")
def ehds_demo_dbt_models(context: AssetExecutionContext) -> Iterator[DbtDagsterEventType]:
    """Build the birth-year summary and infer its column dependencies from compiled SQL."""
    settings = DuckLakeSettings()
    with TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        # Keep the password out of dbt's profile, artifacts, and SQL logs.
        passfile = workdir / "pgpass"
        password = settings.pg_password.get_secret_value().replace("\\", "\\\\").replace(":", "\\:")
        passfile.touch(mode=0o600)
        passfile.write_text(f"{settings.pg_host}:{settings.pg_port}:{settings.pg_db}:{settings.pg_user}:{password}\n")
        dsn = (
            f"host={settings.pg_host} port={settings.pg_port} dbname={settings.pg_db} "
            f"user={settings.pg_user} passfile={passfile}"
        )
        attachment = {
            "path": f"ducklake:postgres:{dsn}",
            "alias": "ducklake",
            "options": {"data_path": str(Path(settings.data_path).resolve()), "override_data_path": True},
        }
        run = _dbt(workdir, attachment).cli(["build"], context=context, target_path=workdir / "target")
        yield from run.stream().fetch_column_metadata()
