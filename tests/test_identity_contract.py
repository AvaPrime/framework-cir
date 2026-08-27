"""Specification tests for M1.6. The binder is a stub.

Implemented behavior (must stay true until a real binder lands):
failure to bind is unbound, never a negative architectural claim.

Cases below document the distinctions a future binder must make.
They are not scored against smolagents.
"""

from framework_cir.identity import IDENTITY_ORDER, bind
from framework_cir.models import Observation


def test_unbound_is_not_negative_evidence() -> None:
    a = Observation("ast_code_match", "write save", "pkg/export.py:1")
    decision = bind(a)
    assert decision.status == "unbound"
    assert decision.identity is None
    assert decision.allows_corroboration() is False


def test_import_alone_does_not_allow_corroboration() -> None:
    a = Observation("import", "mcp", "pkg/tools.py:1")
    decision = bind(a)
    assert decision.allows_corroboration() is False


def test_identity_layers_are_strictly_ordered() -> None:
    assert IDENTITY_ORDER == ("name", "module", "object", "state", "mechanism")


def test_two_saves_do_not_bind_by_verb_alone() -> None:
    a = Observation("ast_code_match", "write save", "pkg/export.py:10")
    b = Observation("ast_code_match", "write save", "pkg/runtime.py:40")
    decision = bind(a, b)
    assert decision.status == "unbound"
    assert decision.allows_corroboration() is False
