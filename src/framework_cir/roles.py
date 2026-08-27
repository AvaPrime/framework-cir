"""M1.7 structural roles. Method names are ignored.

Observation.detail is an access fact:

    ASSIGN <target>
    RETURN <target>

Same owner + ASSIGN and RETURN of the same target → complementary roles.
Same owner + different targets → unbound (distinct state domains).
"""

from __future__ import annotations

import re

from framework_cir.identity import BindDecision, MechanismIdentity, bind
from framework_cir.models import Observation

_ACCESS = re.compile(r"^(ASSIGN|RETURN)\s+(\S+)", re.I)
_OWNER = re.compile(r":(?P<owner>[A-Za-z_][\w]*)\.(?P<member>[A-Za-z_][\w]*)$")


def _owner(obs: Observation) -> str | None:
    m = _OWNER.search(obs.source_location)
    return m.group("owner") if m else None


def _access(obs: Observation) -> tuple[str, str] | None:
    m = _ACCESS.match(obs.detail.strip())
    if not m:
        return None
    return m.group(1).upper(), m.group(2)


def bind_structure(*observations: Observation) -> BindDecision:
    obs = list(observations)
    if len(obs) != 2:
        return BindDecision(
            "insufficient_evidence",
            None,
            "structural binder scores pairs only",
            obs,
        )
    a, b = obs
    oa, ob = _owner(a), _owner(b)
    aa, ab = _access(a), _access(b)
    if not aa or not ab:
        return BindDecision(
            "insufficient_evidence",
            None,
            "missing ASSIGN/RETURN target facts",
            obs,
        )
    if oa and ob and oa != ob:
        return BindDecision("unbound", None, "distinct owners", obs)
    if not oa or not ob:
        return BindDecision(
            "insufficient_evidence",
            None,
            "owner missing",
            obs,
        )
    (dir_a, tgt_a), (dir_b, tgt_b) = aa, ab
    if tgt_a != tgt_b:
        return BindDecision(
            "unbound",
            None,
            f"distinct state domains {tgt_a!r} vs {tgt_b!r}",
            obs,
        )
    if {dir_a, dir_b} == {"ASSIGN", "RETURN"}:
        ident = MechanismIdentity(
            ownership=oa,
            state_domain=tgt_a,
            io_relationship="assign_return",
            evidence_basis=(f"target {tgt_a}", f"dirs {dir_a},{dir_b}"),
            highest_layer="mechanism",
        )
        return BindDecision("bound", ident, "same target assigned and returned", obs)
    return BindDecision(
        "insufficient_evidence",
        None,
        "same target but roles are not assign/return complements",
        obs,
    )


def bind_fallback(*observations: Observation) -> BindDecision:
    """Structure first; never consult identity.bind verb tables unless structure is silent."""
    structured = bind_structure(*observations)
    if structured.status != "insufficient_evidence":
        return structured
    return bind(*observations)
