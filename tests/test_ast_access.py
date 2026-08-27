from pathlib import Path

from framework_cir.ast_access import extract_file
from framework_cir.roles import bind_structure

FIX = Path(__file__).parent / "fixtures" / "roles"


def test_vault_ast_binds() -> None:
    obs = extract_file(FIX / "vault.py")
    details = {o.detail for o in obs}
    assert "ASSIGN self.cells[key]" in details
    assert "RETURN self.cells[key]" in details
    d = bind_structure(obs[0], obs[1])
    assert d.status == "bound"
    assert d.allows_corroboration()


def test_store_ast_binds() -> None:
    obs = extract_file(FIX / "store.py")
    d = bind_structure(*obs)
    assert d.status == "bound"


def test_decoy_cells_vs_log_unbound() -> None:
    obs = [o for o in extract_file(FIX / "decoy.py") if o.source_location.startswith("decoy.py:Vault.")]
    d = bind_structure(*obs)
    assert d.status == "unbound"


def test_extractor_does_not_emit_polarity_verbs() -> None:
    blob = " ".join(o.detail for o in extract_file(FIX / "vault.py"))
    assert "persist" not in blob
    assert "restore" not in blob
    assert "write" not in blob.lower() or "ASSIGN" in blob
