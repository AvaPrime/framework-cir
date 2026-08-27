from framework_cir.models import Observation
from framework_cir.roles import bind_structure


def O(detail: str, loc: str) -> Observation:
    return Observation("ast_code_match", detail, loc)


def test_useless_names_same_cells() -> None:
    d = bind_structure(
        O("ASSIGN self.cells[key]", "vault.py:Vault.a"),
        O("RETURN self.cells[key]", "vault.py:Vault.b"),
    )
    assert d.status == "bound"
    assert d.allows_corroboration()


def test_useless_names_single_slot() -> None:
    d = bind_structure(
        O("ASSIGN self.state", "store.py:Store.q"),
        O("RETURN self.state", "store.py:Store.z"),
    )
    assert d.status == "bound"


def test_same_owner_different_targets() -> None:
    d = bind_structure(
        O("ASSIGN self.cells[key]", "vault.py:Vault.a"),
        O("RETURN self.log[key]", "vault.py:Vault.b"),
    )
    assert d.status == "unbound"
    assert not d.allows_corroboration()


def test_two_assigns_are_not_complements() -> None:
    d = bind_structure(
        O("ASSIGN self.cells[key]", "vault.py:Vault.a"),
        O("ASSIGN self.cells[key]", "vault.py:Vault.c"),
    )
    assert d.status == "insufficient_evidence"


def test_distinct_owners_same_shape() -> None:
    d = bind_structure(
        O("ASSIGN self.cells[key]", "vault.py:Vault.a"),
        O("RETURN self.cells[key]", "other.py:Other.b"),
    )
    assert d.status == "unbound"


def test_method_names_are_not_consulted() -> None:
    d = bind_structure(
        O("ASSIGN self.cells[key]", "vault.py:Vault.save"),
        O("RETURN self.log[key]", "vault.py:Vault.load"),
    )
    assert d.status == "unbound"
