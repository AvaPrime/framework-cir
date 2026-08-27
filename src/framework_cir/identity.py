"""M1.6 identity contract.

Not wired into reconstruct(). bind() has no authority to assert architecture.

Three outcomes, kept separate on purpose:

    bound                  same mechanism justified
    unbound                evidence establishes *different* mechanisms
    insufficient_evidence  identity cannot be established either way

UNBOUND is not INSUFFICIENT_EVIDENCE.
Neither is persistence=false or MCP=unsupported.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from framework_cir.models import Observation

BindStatus = Literal["bound", "unbound", "insufficient_evidence"]

IdentityLayer = Literal["name", "module", "object", "state", "mechanism"]

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
        return (
            self.status == "bound"
            and self.identity is not None
            and self.identity.highest_layer == "mechanism"
        )


def bind(*observations: Observation) -> BindDecision:
    """Identity binder stub.

    Always insufficient_evidence. That is the honest default: the stub cannot
    establish sameness *or* difference. Claiming unbound would be a false
    negative on identity ("these are different mechanisms") without evidence.
    """
    return BindDecision(
        status="insufficient_evidence",
        identity=None,
        reason="identity binder not implemented; cannot establish sameness or difference",
        observations=list(observations),
    )
