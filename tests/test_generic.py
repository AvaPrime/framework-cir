from pathlib import Path

from framework_cir.generic import discover
from framework_cir.extract import LANGGRAPH_RULES

FIXTURES = Path(__file__).parent / "fixtures" / "generic"


def _by_field(report: dict) -> dict:
    return {row["field"]: row for row in report["fields"]}


def test_generic_does_not_consult_signature_tables() -> None:
    assert "StateGraph" in LANGGRAPH_RULES
    report = discover(FIXTURES / "boring_persist")
    blob = str(report)
    assert "StateGraph" not in blob
    assert report["condition"] == "generic"


def test_p1_renamed_persist_restore() -> None:
    fields = _by_field(discover(FIXTURES / "boring_persist"))
    row = fields["memory.persistence_mechanism"]
    assert row["status"] == "supported"
    assert row["value"] == "durable_snapshot"
    assert row["confidence_score"] >= 0.8


def test_branded_readme_does_not_promote_persistence_or_mcp() -> None:
    fields = _by_field(discover(FIXTURES / "branded_empty"))
    persist = fields["memory.persistence_mechanism"]
    mcp = fields["mcp_integration.host_location"]
    assert persist["status"] == "unsupported"
    assert mcp["status"] == "unsupported"
    assert persist["value"] is None
    assert mcp["value"] is None


def test_p2_append_only() -> None:
    fields = _by_field(discover(FIXTURES / "append_log"))
    row = fields["memory.mutation_rule"]
    assert row["status"] == "supported"
    assert row["value"] == "append_only"


def test_p3_p4_graph_builder_without_product_names() -> None:
    fields = _by_field(discover(FIXTURES / "graph_builder"))
    assert fields["routing.topology"]["value"] == "directed_graph"
    assert fields["routing.router_type"]["status"] in {"inferred", "supported"}


def test_p5_p6_protocol_without_saying_mcp() -> None:
    fields = _by_field(discover(FIXTURES / "silent_protocol"))
    assert fields["tool_boundary.present"]["status"] == "supported"
    mcp = fields["mcp_integration.protocol"]
    assert mcp["status"] == "supported"
    assert mcp["value"]["primitives"]["tools"] is True


def test_unknown_when_empty_structure() -> None:
    fields = _by_field(discover(FIXTURES / "branded_empty"))
    assert fields["routing.topology"]["status"] == "unknown"
    assert fields["tool_boundary.present"]["status"] == "unknown"
