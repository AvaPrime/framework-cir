import json
from pathlib import Path

from framework_cir.identity import bind, bind_set
from framework_cir.models import Observation

DATA = json.loads((Path(__file__).parent / "fixtures" / "identity" / "cases_c.json").read_text())


def _parse_spec(spec: str) -> Observation:
    detail, loc = spec.split("@", 1)
    return Observation("ast_code_match", detail, loc)


def test_c1_role_discovery() -> None:
    for case in DATA["c1_pairs"]:
        d = bind(_parse_spec(case["a"]), _parse_spec(case["b"]))
        assert d.status == case["expected"], (case["id"], d.status, d.reason)
        if case["expected"] == "bound":
            assert d.allows_corroboration()
        else:
            assert not d.allows_corroboration()


def test_c2_bag_discovers_two_pairs_and_does_not_reinforce_noise() -> None:
    bag = [Observation(r["kind"], r["detail"], r["source_location"]) for r in DATA["c2_bag"]]
    decisions = bind_set(bag)
    bounds = [d for d in decisions if d.status == "bound"]
    owners = {tuple(sorted(o.source_location for o in d.observations)) for d in bounds}
    assert any("A.write" in " ".join(p) and "A.read" in " ".join(p) for p in owners)
    assert any("B.save" in " ".join(p) and "B.load" in " ".join(p) for p in owners)
    assert len(bounds) == 2
    for d in decisions:
        locs = " ".join(o.source_location for o in d.observations)
        if "Noise.append" in locs:
            assert d.status != "bound"
        if "A.inspect" in locs and d.status == "bound":
            raise AssertionError("inspect must not bind")
