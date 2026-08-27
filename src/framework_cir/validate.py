"""Validate catalog CIR documents against the current schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_TOP = (
    "cir_version",
    "entity_metadata",
    "memory_primitive",
    "routing_primitive",
    "mcp_integration",
    "evidence_anchors",
)

MCP_REQUIRED = (
    "host_location",
    "agent_dsl_field",
    "primitives",
    "transports",
    "tool_filtering",
    "session_model",
    "exposes_agent_as_server",
    "list_changed_subscriptions",
)


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "catalog").is_dir() and (parent / "schema").is_dir():
            return parent
    return Path.cwd()


def validate_doc(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.name}: invalid JSON ({exc})"]
    if not isinstance(data, dict):
        return [f"{path.name}: document must be an object"]
    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"{path.name}: missing {key}")
    mcp = data.get("mcp_integration")
    if isinstance(mcp, dict):
        for key in MCP_REQUIRED:
            if key not in mcp:
                errors.append(f"{path.name}: mcp_integration missing {key}")
        prim = mcp.get("primitives")
        if isinstance(prim, dict):
            for key in ("tools", "resources", "prompts"):
                if key not in prim:
                    errors.append(f"{path.name}: primitives missing {key}")
    anchors = data.get("evidence_anchors")
    if not isinstance(anchors, list) or len(anchors) == 0:
        errors.append(f"{path.name}: evidence_anchors must be a non-empty list")
    return errors


def main() -> int:
    root = repo_root()
    catalog = root / "catalog"
    docs = sorted(catalog.glob("*.json"))
    if not docs:
        print("no catalog documents found", file=sys.stderr)
        return 1
    errors: list[str] = []
    for path in docs:
        errors.extend(validate_doc(path))
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    print(f"ok: {len(docs)} catalog document(s) valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
