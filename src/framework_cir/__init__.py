"""Framework CIR — Canonical Intermediate Representation extractor."""

from framework_cir.evidence import Reconstruction, reconstruct
from framework_cir.extract import (
    AUTOGEN_RULES,
    CIR_VERSION,
    CREWAI_RULES,
    LANGGRAPH_RULES,
    Anchor,
    ScanResult,
    apply_rules,
    emit_cir,
    git_head,
    scan_repo,
)
from framework_cir.generic import discover
from framework_cir.models import FieldRecord, Observation

__all__ = [
    "AUTOGEN_RULES",
    "CIR_VERSION",
    "CREWAI_RULES",
    "LANGGRAPH_RULES",
    "Anchor",
    "FieldRecord",
    "Observation",
    "Reconstruction",
    "ScanResult",
    "apply_rules",
    "discover",
    "emit_cir",
    "git_head",
    "reconstruct",
    "scan_repo",
    "__version__",
]

__version__ = "0.1.0"
