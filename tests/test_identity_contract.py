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


def test_lone_observation_is_insufficient() -> None:
    decision = bind(Observation("ast_code_match", "write save", "pkg/export.py:save"))
    assert decision.status == "insufficient_evidence"
    assert decision.allows_corroboration() is False


def test_identity_layers_are_strictly_ordered() -> None:
    assert IDENTITY_ORDER == ("name", "module", "object", "state", "mechanism")


def test_binder_matches_synthetic_corpus() -> None:
    got = {}
    for case in CASES:
        decision = bind(*(_obs(case["a"]) + _obs(case.get("b"))))
        got[case["id"]] = decision.status
        assert decision.status == case["expected"], (
            case["id"],
            decision.status,
            decision.reason,
        )
        if case["expected"] == "bound":
            assert decision.allows_corroboration()
        else:
            assert not decision.allows_corroboration()
    assert got["same-mechanism-different-names"] == "bound"
    assert got["agent-export-vs-config-save"] == "unbound"
    assert got["lone-save"] == "insufficient_evidence"
