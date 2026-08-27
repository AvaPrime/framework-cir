"""Shared records for signature control and generic discovery."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

FieldStatus = Literal[
    "observed",
    "inferred",
    "supported",
    "unsupported",
    "unknown",
    "contradicted",
]

EvidenceChannel = Literal[
    "ast_code_match",
    "ast_call",
    "ast_attribute",
    "string_literal",
    "import",
    "readme_text",
    "docstring",
]


@dataclass
class Observation:
    kind: EvidenceChannel
    detail: str
    source_location: str
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        row: dict[str, Any] = {
            "kind": self.kind,
            "detail": self.detail,
            "source_location": self.source_location,
        }
        if self.extra:
            row["extra"] = self.extra
        return row


@dataclass
class FieldRecord:
    field: str
    value: Any
    status: FieldStatus
    confidence_score: float
    interpretation: str
    rule: str
    observations: list[Observation] = field(default_factory=list)
    rejected: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "field": self.field,
            "value": self.value,
            "status": self.status,
            "confidence_score": self.confidence_score,
            "derivation": {
                "observations": [o.to_dict() for o in self.observations],
                "interpretation": self.interpretation,
                "rule": self.rule,
                "rejected_channels": self.rejected,
            },
        }
