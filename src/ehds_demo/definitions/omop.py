"""OMOP CDM definitions.

Bundles all OMOP-related assets into a single Definitions object.
Use this as a code location for stations that follow the OMOP CDM::

    dagster dev -m ehds_demo.definitions.omop
"""

from dagster import AssetKey, Definitions, define_asset_job
from pluginlake.core.ducklake.io_manager import ducklake_io_manager

from ehds_demo.assets.dbt_models import ehds_demo_dbt_models
from ehds_demo.assets.omop import (
    CLINICAL_TABLES,
    VOCABULARY_TABLES,
    omop_clinical_tables,
    omop_raw_clinical_tables,
    omop_vocabulary_tables,
)
from ehds_demo.assets.omop_sensor import omop_folder_sensor
from ehds_demo.assets.omop_vocab_sensor import omop_vocab_sensor

omop_ingest_job = define_asset_job(
    name="omop_ingest_job",
    selection=[AssetKey(["omop_raw", t]) for t in CLINICAL_TABLES] + [AssetKey(["omop", t]) for t in CLINICAL_TABLES],
)

omop_vocab_ingest_job = define_asset_job(
    name="omop_vocab_ingest_job",
    selection=[AssetKey(["omop_vocab", t]) for t in VOCABULARY_TABLES],
)

defs = Definitions(
    assets=[omop_raw_clinical_tables, omop_clinical_tables, omop_vocabulary_tables, ehds_demo_dbt_models],
    jobs=[
        omop_ingest_job,
        omop_vocab_ingest_job,
        define_asset_job("dbt_birth_year_demo", selection=[ehds_demo_dbt_models]),
    ],
    sensors=[omop_folder_sensor, omop_vocab_sensor],
    resources={"io_manager": ducklake_io_manager},
)
