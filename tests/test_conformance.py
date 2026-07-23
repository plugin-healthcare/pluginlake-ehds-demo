"""Conformance test for ehds-demo.

Verifies the project manifest passes the pluginlake conformance suite, so
regressions in the plugin contract are caught in the project's own CI.
"""

from pluginlake.plugins.conformance import verify_manifest

from ehds_demo.manifest import manifest


def test_manifest_conforms() -> None:
    issues = verify_manifest(manifest)
    assert issues == [], "\n".join(str(i) for i in issues)
