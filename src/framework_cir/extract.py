#!/usr/bin/env python3
"""Minimal Layer 1-3 CIR extractor.

Hybrid design:
  1. Walk a local repo and collect AST anchors.
  2. Match anchors against framework-specific rule tables.
  3. Emit CIR v1.0.2 documents. LLM labeling is optional and never overrides an AST-corroborated field.
"""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CIR_VERSION = "1.0.2"


@dataclass
class Anchor:
    claim: str
    evidence_type: str
    confidence_score: float
    source_location: str


@dataclass
class ScanResult:
    classes: set[str] = field(default_factory=set)
    functions: set[str] = field(default_factory=set)
    imports: set[str] = field(default_factory=set)
    name_hits: list[tuple[str, str]] = field(default_factory=list)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head(repo: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    except Exception:
        return "unknown"


def parse_py(path: Path) -> tuple[set[str], set[str], set[str]]:
    classes, functions, imports = set(), set(), set()
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError:
        return classes, functions, imports
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.add(node.name)
        elif isinstance(node, ast.FunctionDef):
            functions.add(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
            for alias in node.names:
                imports.add(alias.name)
    return classes, functions, imports


def scan_repo(root: Path, max_files: int = 4000) -> ScanResult:
    result = ScanResult()
    count = 0
    for path in root.rglob("*.py"):
        if any(part in {".git", "tests", "test", "examples", "docs"} for part in path.parts):
            continue
        count += 1
        if count > max_files:
            break
        classes, functions, imports = parse_py(path)
        result.classes |= classes
        result.functions |= functions
        result.imports |= imports
        rel = str(path.relative_to(root))
        for name in classes:
            result.name_hits.append((name, rel))
    return result


LANGGRAPH_RULES = {
    "StateGraph": ("memory.architecture_model", "state_graph", 0.99),
    "SqliteSaver": ("memory.persistence_mechanism", "sqlite_checkpoint", 0.98),
    "PostgresSaver": ("memory.persistence_mechanism", "postgres_checkpoint", 0.95),
    "BinaryOperatorAggregate": ("memory.mutation_rule", "reducer_merge", 0.96),
    "add_conditional_edges": ("routing.router_type", "static_conditional_edge", 0.97),
    "interrupt_before": ("routing.cycle_recovery_mechanism", "human_in_the_loop_interrupt", 0.94),
    "MCPServerStdio": ("mcp.host_location", "adapter_or_in_tree", 0.70),
}

CREWAI_RULES = {
    "Memory": ("memory.architecture_model", "hybrid", 0.90),
    "MemoryRecord": ("memory.architecture_model", "hybrid", 0.88),
    "LanceDB": ("memory.persistence_mechanism", "vector_db", 0.92),
    "lancedb": ("memory.persistence_mechanism", "vector_db", 0.92),
    "Process": ("routing.topology", "hierarchical_swarm", 0.80),
    "MCPServerHTTP": ("mcp.host_location", "in_tree", 0.95),
    "MCPServerStdio": ("mcp.host_location", "in_tree", 0.95),
}

AUTOGEN_RULES = {
    "ListMemory": ("memory.architecture_model", "message_log", 0.95),
    "Memory": ("memory.architecture_model", "message_log", 0.70),
    "AssistantAgent": ("routing.router_type", "llm_decision_node", 0.80),
}


def apply_rules(scan: ScanResult, rules: dict[str, tuple[str, str, float]]) -> list[Anchor]:
    symbols = scan.classes | scan.functions | scan.imports
    symbol_l = {s.lower() for s in symbols}
    hits: dict[str, str] = {name.lower(): path for name, path in scan.name_hits}
    anchors: list[Anchor] = []
    for symbol, (claim_field, value, conf) in rules.items():
        present = symbol in symbols or symbol.lower() in symbol_l
        if not present:
            continue
        loc = hits.get(symbol.lower(), "repo-wide symbol match")
        anchors.append(
            Anchor(
                claim=f"{claim_field} = {value}",
                evidence_type="ast_code_match",
                confidence_score=conf,
                source_location=loc,
            )
        )
    return anchors


def emit_cir(
    name: str,
    version: str,
    source_url: str,
    commit: str,
    memory: dict[str, Any],
    routing: dict[str, Any],
    anchors: list[Anchor],
    out_path: Path,
    mcp_integration: dict[str, Any] | None = None,
) -> Path:
    doc = {
        "cir_version": CIR_VERSION,
        "entity_metadata": {
            "name": name,
            "version": version,
            "commit_hash": commit,
            "source_url": source_url,
            "analyzed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "extraction_metadata": {
            "ast_parser": "python-ast",
            "llm_model": "none",
            "corroboration_rules_version": "1.0.0",
        },
        "memory_primitive": memory,
        "routing_primitive": routing,
        "mcp_integration": mcp_integration or {
            "host_location": "none",
            "agent_dsl_field": "none",
            "primitives": {"tools": False, "resources": False, "prompts": False},
            "transports": [],
            "tool_filtering": "none",
            "session_model": "none",
            "exposes_agent_as_server": False,
            "list_changed_subscriptions": False,
            "package": None,
        },
        "evidence_anchors": [
            {
                "claim": a.claim,
                "evidence_type": a.evidence_type,
                "confidence_score": a.confidence_score,
                "source_location": a.source_location,
            }
            for a in anchors
        ],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    return out_path
