"""Framework CIR — Canonical Intermediate Representation extractor."""

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

__all__ = [
    "AUTOGEN_RULES",
    "CIR_VERSION",
    "CREWAI_RULES",
    "LANGGRAPH_RULES",
    "Anchor",
    "ScanResult",
    "apply_rules",
    "emit_cir",
    "git_head",
    "scan_repo",
    "__version__",
]

__version__ = "0.1.0"
