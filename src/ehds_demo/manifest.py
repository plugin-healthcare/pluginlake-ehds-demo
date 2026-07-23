"""Project manifest for ehds-demo.

The single registration surface for this project (ADR-009). Core discovers it
through the ``pluginlake.projects`` entry point and wires the declared OMOP and
FHIR code locations and API routers uniformly. This mirrors the former in-tree
registration exactly, so the split preserves today's behaviour.
"""

from pluginlake.plugins.manifest import CodeLocationSpec, ProjectManifest, RouterSpec

manifest = ProjectManifest(
    id="ehds-demo",
    catalog="ducklake",
    namespace="ehds-demo",
    config_prefix="EHDS_DEMO_",
    requires_core=">=0.1.0,<0.2.0",
    code_locations=[
        CodeLocationSpec(module="ehds_demo.definitions.omop"),
        CodeLocationSpec(module="ehds_demo.definitions.fhir"),
    ],
    routers=[
        RouterSpec(module="ehds_demo.api.routers.omop"),
        RouterSpec(module="ehds_demo.api.routers.omop_statistics"),
        RouterSpec(module="ehds_demo.api.routers.fhir"),
        RouterSpec(module="ehds_demo.api.routers.fhir_statistics"),
    ],
)
