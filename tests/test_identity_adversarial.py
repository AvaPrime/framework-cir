import json
from pathlib import Path

from framework_cir.identity import bind
from framework_cir.models import Observation

CASES = json.loads(
    (Path(__file__).parent / "fixtures" / "identity" / "cases_adversarial.json").read_text()
)["cases"]


def _rows(case: dict) -> list[Observation]:
    if "observations" in case:
        return [Observation(r["kind"], r["detail"], r["source_location"]) for r in case["observations"]]
    out = []
    for key in ("a", "b"):
        row = case.get(key)
        if row:
            out.append(Observation(row["kind"], row["detail"], row["source_location"]))
    return out


def test_adversarial_corpus_reports_each_case() -> None:
    """Does not require 8/8. Records binder vs theory for SCORE.md."""
    report = {}
    for case in CASES:
        decision = bind(*_rows(case))
        report[case["id"]] = {
            "expected": case["expected"],
            "got": decision.status,
            "ok": decision.status == case["expected"],
        }
    # Original-style easy variants must still hold.
    assert report["reordered-persist-restore"]["ok"]
    assert report["renamed-owner"]["ok"]
    assert report["nested-module-path"]["ok"]
    assert report["write-read-unlisted-verbs"]["ok"]
    assert report["partial-owner"]["ok"]
    assert report["extra-same-verb-other-owner"]["ok"]
    # Hard variants are measured, not required yet:
    # unlisted-verbs-only, pair-plus-noise
    print(report)
