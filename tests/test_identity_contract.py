import json
from pathlib import Path

from framework_cir.identity import IDENTITY_ORDER, bind
from framework_cir.models import Observation

CASES = json.loads(
    (Path(__file__).parent / "fixtures" / "identity" / "cases.json").read_text()
)["cases"]


def _obs(row: dict | None) -> list[Observation]:
    if row is None:
        return []
    return [Observation(row["kind"], row["detail"], row["source_location"])]


def test_stub_is_insufficient_not_unbound() -> None:
    a = Observation("ast_code_match", "write save", "pkg/export.py:1")
    b = Observation("ast_code_match", "read restore", "pkg/runtime.py:1")
    decision = bind(a, b)
    assert decision.status == "insufficient_evidence"
    assert decision.identity is None
    assert decision.allows_corroboration() is False


def test_lone_observation_is_insufficient() -> None:
    decision = bind(Observation("import", "mcp", "tools.py:1"))
    assert decision.status == "insufficient_evidence"
    assert decision.allows_corroboration() is False


def test_identity_layers_are_strictly_ordered() -> None:
    assert IDENTITY_ORDER == ("name", "module", "object", "state", "mechanism")


def test_corpus_expected_labels_are_the_three_outcomes() -> None:
    allowed = {"bound", "unbound", "insufficient_evidence"}
    assert {c["expected"] for c in CASES} <= allowed
    assert {c["expected"] for c in CASES} == allowed


def test_stub_does_not_implement_the_corpus() -> None:
    """Guard: a stub that starts returning bound has started smuggling results."""
    for case in CASES:
        obs = _obs(case["a"]) + _obs(case.get("b"))
        decision = bind(*obs)
        assert decision.status == "insufficient_evidence", case["id"]
        assert decision.allows_corroboration() is False
