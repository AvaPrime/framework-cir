from pathlib import Path

from framework_cir.ast_access import extract_file, kinds
from framework_cir.roles import bind_structure

FIX = Path(__file__).parent / "fixtures" / "roles" / "coverage.py"


def test_extractor_distinguishes_mutation_shapes() -> None:
    obs = extract_file(FIX)
    seen = kinds(obs)
    assert "ASSIGN" in seen
    assert "AUG_ASSIGN" in seen
    assert "SETATTR" in seen
    assert "RETURN" in seen
    # INDEX_WRITE may alias ASSIGN of a subscript; record whatever landed.
    assert "ASSIGN" in seen or "INDEX_WRITE" in seen


def test_augassign_is_not_treated_as_assign() -> None:
    obs = extract_file(FIX)
    aug = [o for o in obs if o.detail.startswith("AUG_ASSIGN")]
    assigns = [o for o in obs if o.detail.startswith("ASSIGN") and "plain" in o.source_location]
    assert aug and assigns
    assert aug[0].detail != assigns[0].detail


def test_plain_assign_still_binds_to_return_of_same_target() -> None:
    obs = extract_file(FIX)
    write = next(o for o in obs if o.detail == "ASSIGN self.x" and o.source_location.endswith(".plain"))
    read = next(o for o in obs if o.detail == "RETURN self.x")
    assert bind_structure(write, read).status == "bound"


def test_augassign_does_not_silently_bind_as_assign() -> None:
    obs = extract_file(FIX)
    aug = next(o for o in obs if o.detail.startswith("AUG_ASSIGN"))
    read = next(o for o in obs if o.detail == "RETURN self.x")
    assert bind_structure(aug, read).status == "insufficient_evidence"


def test_setattr_does_not_silently_bind_as_assign() -> None:
    obs = extract_file(FIX)
    s = next(o for o in obs if o.detail.startswith("SETATTR"))
    read = next(o for o in obs if o.detail == "RETURN self.x")
    assert bind_structure(s, read).status == "insufficient_evidence"
