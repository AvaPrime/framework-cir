"""Evidence graph: observations and relationships; CIR is a projection.

P1–P6 remain analysis passes. They emit FieldRecords. This module lifts those
records into a graph so Run A can inspect composition, not only the projection.

Relation kinds
  SUPPORTS      observation → field candidate
  CORROBORATES  observation/field → observation/field
  CONTRADICTS   observation → field (claim vs missing structure)
  DERIVES       observation set → asserted field
  REJECTS       documentation observation not promoted
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from framework_cir.generic import DETECTORS, collect_facts
from framework_cir.models import FieldRecord, Observation

RelKind = Literal["supports", "corroborates", "contradicts", "derives", "rejects"]


@dataclass
class Relation:
    kind: RelKind
    src: str
    dst: str
    note: str = ""

    def to_dict(self) -> dict[str, str]:
        row = {"kind": self.kind, "src": self.src, "dst": self.dst}
        if self.note:
            row["note"] = self.note
        return row


@dataclass
class Reconstruction:
    """Stable query surface. Callers should not care which detector fired."""

    root: str
    observations: list[tuple[str, Observation]] = field(default_factory=list)
    relationships: list[Relation] = field(default_factory=list)
    fields: list[FieldRecord] = field(default_factory=list)

    @property
    def evidence(self) -> list[dict[str, Any]]:
        return [{"id": oid, **obs.to_dict()} for oid, obs in self.observations]

    @property
    def derivations(self) -> list[dict[str, Any]]:
        return [f.to_dict() for f in self.fields]

    def field_map(self) -> dict[str, FieldRecord]:
        return {f.field: f for f in self.fields}

    def to_discover_dict(self) -> dict[str, Any]:
        return {
            "experiment": "CIR-HOLDOUT-001",
            "condition": "generic",
            "root": self.root,
            "files_scanned": None,
            "fields": [f.to_dict() for f in self.fields],
            "evidence_graph": {
                "observations": self.evidence,
                "relationships": [r.to_dict() for r in self.relationships],
            },
        }


def _obs_id(prefix: str, index: int) -> str:
    return f"{prefix}:obs:{index}"


def reconstruct(root: Path) -> Reconstruction:
    """Run generic analyzers and project an evidence graph.

    Does not consult signature tables. Does not select a holdout.
    """
    facts = collect_facts(root)
    fields = [fn(facts) for fn in DETECTORS.values()]
    project = Reconstruction(root=str(root), fields=fields)

    obs_index = 0
    field_ids: dict[str, str] = {}
    for rec in fields:
        fid = f"field:{rec.field}"
        field_ids[rec.field] = fid
        for obs in rec.observations:
            oid = _obs_id(rec.field, obs_index)
            obs_index += 1
            project.observations.append((oid, obs))
            if rec.status in {"supported", "inferred", "observed"}:
                project.relationships.append(
                    Relation("supports", oid, fid, rec.interpretation)
                )
                if rec.status == "supported":
                    project.relationships.append(Relation("derives", oid, fid, rec.rule))
            if rec.status == "unsupported" and obs.kind == "readme_text":
                project.relationships.append(
                    Relation(
                        "rejects",
                        oid,
                        fid,
                        "documentation claim not promoted to architecture",
                    )
                )
                project.relationships.append(
                    Relation("contradicts", oid, fid, rec.interpretation)
                )

    fmap = project.field_map()
    tools = fmap.get("tool_boundary.present")
    mcp_ok = fmap.get("mcp_integration.protocol")
    mcp_doc = fmap.get("mcp_integration.host_location")
    if tools and tools.status == "supported" and mcp_ok and mcp_ok.status == "supported":
        project.relationships.append(
            Relation(
                "corroborates",
                field_ids["tool_boundary.present"],
                field_ids["mcp_integration.protocol"],
                "capability boundary is protocol-shaped",
            )
        )
    if (
        tools
        and tools.status in {"unknown", "unsupported"}
        and mcp_doc
        and mcp_doc.status == "unsupported"
    ):
        project.relationships.append(
            Relation(
                "corroborates",
                field_ids["tool_boundary.present"],
                field_ids["mcp_integration.host_location"],
                "no tool surface and no protocol — doc-only MCP stays unsupported",
            )
        )
    persist = fmap.get("memory.persistence_mechanism")
    if persist and persist.status == "supported":
        writes = [oid for oid, o in project.observations if o.detail.startswith("write ")]
        reads = [oid for oid, o in project.observations if o.detail.startswith("read ")]
        for w in writes:
            for r in reads:
                project.relationships.append(
                    Relation("corroborates", w, r, "write/read pair under an identity")
                )
    return project
