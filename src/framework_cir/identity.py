"""M1.6 identity contract.

Not a detector. Not wired into reconstruct(). Binding is unimplemented on
purpose: failure to bind must remain unknown, never negative evidence.

Predicates (all required before corroborates(A, B) is legal):

    same_mechanism(A, B)
    AND complementary_role(A, B)
    AND compatible_scope(A, B)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from framework_cir.models import Observation

BindStatus = Literal["bound", "unbound", "contradicted"]

IdentityLayer = Literal[
    "name",
    "module",
    "object",
    "state",
    "mechanism",
]

# Hierarchy: same name ≠ same module ≠ same object ≠ same state ≠ same mechanism
IDENTITY_ORDER: tuple[IdentityLayer, ...] = (
    "name",
    "module",
    "object",
    "state",
    "mechanism",
)


@dataclass(frozen=True)
class MechanismIdentity:
    subject_scope: str | None = None
    ownership: str | None = None
    execution_context: str | None = None
    state_domain: str | None = None
    io_relationship: str | None = None
    lifecycle_relationship: str | None = None
    temporal_relationship: str | None = None
    evidence_basis: tuple[str, ...] = ()
    highest_layer: IdentityLayer = "name"

    def to_dict(self) -> dict:
        return {
            "subject_scope": self.subject_scope,
            "ownership": self.ownership,
            "execution_context": self.execution_context,
            "state_domain": self.state_domain,
            "io_relationship": self.io_relationship,
            "lifecycle_relationship": self.lifecycle_relationship,
            "temporal_relationship": self.temporal_relationship,
            "evidence_basis": list(self.evidence_basis),
            "highest_layer": self.highest_layer,
        }


@dataclass
class BindDecision:
    status: BindStatus
    identity: MechanismIdentity | None
    reason: str
    observations: list[Observation] = field(default_factory=list)

    def allows_corroboration(self) -> bool:
        return self.status == "bound" and self.identity is not None and self.identity.highest_layer == "mechanism"


def bind(*observations: Observation) -> BindDecision:
    """Identity binder.

    Current implementation always returns unbound. That is the correct default:
    an unbound pair must not become persistence=false or MCP=unsupported.
    """
    return BindDecision(
        status="unbound",
        identity=None,
        reason="identity binder not implemented; observations remain observations",
        observations=list(observations),
    )
