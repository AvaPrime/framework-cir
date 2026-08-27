from pathlib import Path

from framework_cir.evidence import reconstruct
from framework_cir.extract import LANGGRAPH_RULES

FIXTURES = Path(__file__).parent / "fixtures" / "generic"


def test_reconstruct_does_not_use_signatures() -> None:
    assert "StateGraph" in LANGGRAPH_RULES
    project = reconstruct(FIXTURES / "boring_persist")
    blob = str(project.to_discover_dict())
    assert "StateGraph" not in blob


def test_p1_write_read_corroborate() -> None:
    project = reconstruct(FIXTURES / "boring_persist")
    assert any(r.kind == "corroborates" and "write/read" in r.note for r in project.relationships)
    persist = project.field_map()["memory.persistence_mechanism"]
    assert persist.status == "supported"
    assert any(r.kind == "derives" for r in project.relationships)


def test_branded_readme_is_rejected_not_promoted() -> None:
    project = reconstruct(FIXTURES / "branded_empty")
    assert any(r.kind == "rejects" for r in project.relationships)
    assert any(r.kind == "contradicts" for r in project.relationships)
    persist = project.field_map()["memory.persistence_mechanism"]
    mcp = project.field_map()["mcp_integration.host_location"]
    assert persist.status == "unsupported"
    assert mcp.status == "unsupported"
    assert persist.value is None


def test_p5_corroborates_p6_when_protocol_present() -> None:
    project = reconstruct(FIXTURES / "silent_protocol")
    assert any(
        r.kind == "corroborates" and "protocol-shaped" in r.note for r in project.relationships
    )
    assert project.field_map()["mcp_integration.protocol"].status == "supported"


def test_projection_does_not_replace_evidence() -> None:
    project = reconstruct(FIXTURES / "silent_protocol")
    assert project.observations
    assert project.relationships
    assert project.fields
    dumped = project.to_discover_dict()
    assert "evidence_graph" in dumped
    assert dumped["fields"]
