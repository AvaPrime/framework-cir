"""M1.6 identity binder.

Uses only Observation.{kind, detail, source_location}.
No product vocabulary. Not wired into reconstruct().
"""

from __future__ import annotations

import re
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

_LOC = re.compile(
    r"^(?P<module>[^:]+)(?::(?P<owner>[A-Za-z_][\w]*)\.(?P<member>[A-Za-z_][\w]*))?$"
)

# Role pairs that are complementary in structure, not in product branding.
_COMPLEMENTS = {
    frozenset({"write", "read"}),
    frozenset({"persist", "restore"}),
    frozenset({"put", "get"}),
    frozenset({"checkpoint", "resume"}),
    frozenset({"tools/list", "tools/call"}),
    frozenset({"list_tools", "call_tool"}),
}


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


@dataclass(frozen=True)
class _Parsed:
    module: str
    owner: str | None
    member: str | None
    kind: str
    tokens: frozenset[str]


def _tokens(detail: str) -> frozenset[str]:
    parts = set(re.split(r"[\s._]+", detail.lower()))
    parts.add(detail.lower())
    return frozenset(p for p in parts if p)


def _parse(obs: Observation) -> _Parsed:
    m = _LOC.match(obs.source_location.strip())
    if not m:
        return _Parsed(obs.source_location, None, None, obs.kind, _tokens(obs.detail))
    return _Parsed(
        m.group("module"),
        m.group("owner"),
        m.group("member"),
        obs.kind,
        _tokens(obs.detail),
    )


def _complementary(a: _Parsed, b: _Parsed) -> bool:
    combo = a.tokens | b.tokens
    return any(pair <= combo for pair in _COMPLEMENTS)


def bind(*observations: Observation) -> BindDecision:
    obs = list(observations)
    if len(obs) < 2:
        return BindDecision(
            "insufficient_evidence",
            None,
            "fewer than two observations; cannot establish sameness or difference",
            obs,
        )
    if len(obs) > 2:
        return BindDecision(
            "insufficient_evidence",
            None,
            "binder scores pairs only",
            obs,
        )

    left, right = _parse(obs[0]), _parse(obs[1])

    if {left.kind, right.kind} == {"readme_text", "ast_code_match"} or (
        "readme_text" in {left.kind, right.kind} and left.module != right.module
    ):
        return BindDecision(
            "unbound",
            None,
            "documentation and implementation do not share an owner",
            obs,
        )

    if {left.kind, right.kind} == {"import", "ast_code_match"} and left.module != right.module:
        return BindDecision(
            "unbound",
            None,
            "import token and unrelated client live in different modules",
            obs,
        )

    if left.owner and right.owner and left.owner != right.owner:
        return BindDecision(
            "unbound",
            None,
            f"distinct owners {left.owner!r} vs {right.owner!r}",
            obs,
        )

    if left.owner and right.owner and left.owner == right.owner and _complementary(left, right):
        ident = MechanismIdentity(
            subject_scope=left.module,
            ownership=left.owner,
            state_domain=left.owner,
            io_relationship="complementary",
            lifecycle_relationship="paired",
            evidence_basis=(
                f"same owner {left.owner}",
                f"modules {left.module},{right.module}",
                f"roles {sorted(left.tokens & _flatten_roles())} / {sorted(right.tokens & _flatten_roles())}",
            ),
            highest_layer="mechanism",
        )
        return BindDecision("bound", ident, "same owner and complementary roles", obs)

    return BindDecision(
        "insufficient_evidence",
        None,
        "no justified same-owner complementary pair and no justified distinct-owner split",
        obs,
    )


def _flatten_roles() -> frozenset[str]:
    out: set[str] = set()
    for pair in _COMPLEMENTS:
        out.update(pair)
    return frozenset(out)
