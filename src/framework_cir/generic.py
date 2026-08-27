"""Generic structural detectors (CIR-HOLDOUT-001 experimental condition).

No framework product names. No catalog knowledge. Lexical cues are limited to
ordinary persistence/routing/protocol vocabulary, then corroborated structurally.

P1 Persistence — durable write + read + identity
P2 Mutation    — how state becomes next state
P3 Topology    — how control is wired
P4 Routing     — what selects the next target
P5 Tools       — capability boundary (name + schema + invoke)
P6 MCP         — whether that boundary is protocol-shaped
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path

from framework_cir.models import FieldRecord, Observation

WRITE_HINTS = {
    "save", "persist", "store", "dump", "write", "put",
    "checkpoint", "snapshot", "serialize",
}
READ_HINTS = {
    "load", "restore", "fetch", "read", "get", "resume",
    "deserialize", "reload",
}
IDENTITY_HINTS = {
    "id", "key", "uid", "token", "identity", "run_id",
    "session_id", "thread_id", "path",
}
MCP_METHODS = {
    "tools/list", "tools/call", "resources/list", "resources/read",
    "prompts/list", "prompts/get", "notifications/initialized", "initialize",
}
DOC_MCP_PHRASES = ("mcp", "model context protocol")
DOC_PERSIST_PHRASES = ("persistent memory", "native memory", "checkpoint")


@dataclass
class _Func:
    name: str
    args: list[str]
    calls: set[str]
    location: str
    returns_name: bool = False
    has_append: bool = False
    has_update: bool = False
    string_lits: set[str] = field(default_factory=set)


@dataclass
class _Class:
    name: str
    methods: dict[str, _Func]
    location: str
    bases: list[str]


@dataclass
class RepoFacts:
    classes: list[_Class] = field(default_factory=list)
    functions: list[_Func] = field(default_factory=list)
    imports: set[str] = field(default_factory=set)
    string_lits: set[str] = field(default_factory=set)
    readme_text: str = ""
    files: list[str] = field(default_factory=list)


def _func_from_def(node: ast.FunctionDef | ast.AsyncFunctionDef, location: str) -> _Func:
    args = [a.arg for a in node.args.args]
    calls: set[str] = set()
    lits: set[str] = set()
    has_append = False
    has_update = False
    returns_name = False
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            if isinstance(child.func, ast.Name):
                calls.add(child.func.id)
            elif isinstance(child.func, ast.Attribute):
                calls.add(child.func.attr)
                if child.func.attr == "append":
                    has_append = True
                if child.func.attr == "update":
                    has_update = True
        elif isinstance(child, ast.Constant) and isinstance(child.value, str):
            lits.add(child.value)
        elif isinstance(child, ast.Return) and isinstance(child.value, ast.Name):
            returns_name = True
    return _Func(
        name=node.name,
        args=args,
        calls=calls,
        location=f"{location}:{node.lineno}",
        returns_name=returns_name,
        has_append=has_append,
        has_update=has_update,
        string_lits=lits,
    )


def collect_facts(root: Path, max_files: int = 4000) -> RepoFacts:
    facts = RepoFacts()
    readme = root / "README.md"
    if readme.is_file():
        facts.readme_text = readme.read_text(encoding="utf-8", errors="ignore")
    count = 0
    for path in root.rglob("*.py"):
        if any(part in {".git", ".venv", "venv", "__pycache__"} for part in path.parts):
            continue
        count += 1
        if count > max_files:
            break
        rel = str(path.relative_to(root))
        facts.files.append(rel)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    facts.imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                facts.imports.add(node.module.split(".")[0])
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                facts.string_lits.add(node.value)
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                methods = {}
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods[item.name] = _func_from_def(item, rel)
                facts.classes.append(
                    _Class(
                        name=node.name,
                        methods=methods,
                        location=f"{rel}:{node.lineno}",
                        bases=[
                            b.id if isinstance(b, ast.Name) else ast.unparse(b)
                            for b in node.bases
                        ],
                    )
                )
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                facts.functions.append(_func_from_def(node, rel))
    return facts


def _hint_hit(name: str, hints: set[str]) -> bool:
    lower = name.lower()
    return any(h in lower for h in hints)


def _has_identity(args: list[str]) -> bool:
    lowered = {a.lower() for a in args}
    return bool(lowered & IDENTITY_HINTS) or any(
        any(h in a.lower() for h in IDENTITY_HINTS) for a in args
    )


def detect_p1(facts: RepoFacts) -> FieldRecord:
    writes: list[_Func] = []
    reads: list[_Func] = []
    for cls in facts.classes:
        for fn in cls.methods.values():
            if _hint_hit(fn.name, WRITE_HINTS) and _has_identity(fn.args):
                writes.append(fn)
            if _hint_hit(fn.name, READ_HINTS) and _has_identity(fn.args):
                reads.append(fn)
    for fn in facts.functions:
        if _hint_hit(fn.name, WRITE_HINTS) and _has_identity(fn.args):
            writes.append(fn)
        if _hint_hit(fn.name, READ_HINTS) and _has_identity(fn.args):
            reads.append(fn)

    doc_hits = [phrase for phrase in DOC_PERSIST_PHRASES if phrase in facts.readme_text.lower()]
    rejected: list[dict[str, str]] = []
    if doc_hits and not (writes and reads):
        rejected.append({
            "channel": "readme_text",
            "claim": ", ".join(doc_hits),
            "reason": "documentation claim without matching write/read pair",
        })

    if writes and reads:
        obs = [Observation("ast_code_match", f"write {w.name}", w.location) for w in writes[:3]]
        obs += [Observation("ast_code_match", f"read {r.name}", r.location) for r in reads[:3]]
        return FieldRecord(
            field="memory.persistence_mechanism",
            value="durable_snapshot",
            status="supported",
            confidence_score=0.86,
            interpretation="execution state is written and later read under an identity",
            rule="durable_snapshot = write_hint + read_hint + identity_arg",
            observations=obs,
            rejected=rejected,
        )
    if writes or reads:
        side = writes or reads
        return FieldRecord(
            field="memory.persistence_mechanism",
            value="partial_snapshot",
            status="inferred",
            confidence_score=0.45,
            interpretation="one side of a persist pair exists; durable snapshot is not corroborated",
            rule="durable_snapshot requires both write and read",
            observations=[Observation("ast_code_match", f"{s.name}", s.location) for s in side[:4]],
            rejected=rejected,
        )
    if doc_hits:
        return FieldRecord(
            field="memory.persistence_mechanism",
            value=None,
            status="unsupported",
            confidence_score=0.2,
            interpretation="persistence is claimed in documentation only",
            rule="docs cannot promote a structural field",
            observations=[Observation("readme_text", phrase, "README.md") for phrase in doc_hits],
            rejected=rejected,
        )
    return FieldRecord(
        field="memory.persistence_mechanism",
        value=None,
        status="unknown",
        confidence_score=0.0,
        interpretation="no durable snapshot triad observed",
        rule="durable_snapshot = write_hint + read_hint + identity_arg",
    )


def detect_p2(facts: RepoFacts) -> FieldRecord:
    appends: list[Observation] = []
    updates: list[Observation] = []
    reducers: list[Observation] = []
    for fn in [*facts.functions, *[m for c in facts.classes for m in c.methods.values()]]:
        if fn.has_append:
            appends.append(Observation("ast_attribute", f"{fn.name} calls append", fn.location))
        if fn.has_update:
            updates.append(Observation("ast_attribute", f"{fn.name} calls update", fn.location))
        argset = {a.lower() for a in fn.args}
        if {"current", "update"} <= argset or {"state", "delta"} <= argset or {"old", "new"} <= argset:
            reducers.append(Observation("ast_code_match", f"{fn.name}({', '.join(fn.args)})", fn.location))
    if reducers:
        return FieldRecord(
            field="memory.mutation_rule",
            value="reducer_merge",
            status="inferred",
            confidence_score=0.62,
            interpretation="a function takes prior state plus a delta",
            rule="reducer_shape = (current|state|old) + (update|delta|new)",
            observations=reducers[:5],
        )
    if appends and not updates:
        return FieldRecord(
            field="memory.mutation_rule",
            value="append_only",
            status="supported",
            confidence_score=0.72,
            interpretation="state grows by append",
            rule="append_only = .append() without reducer pair",
            observations=appends[:5],
        )
    if updates:
        return FieldRecord(
            field="memory.mutation_rule",
            value="overwrite_merge",
            status="inferred",
            confidence_score=0.58,
            interpretation="state is mutated in place via update",
            rule="overwrite_merge = .update()",
            observations=updates[:5],
        )
    return FieldRecord(
        field="memory.mutation_rule",
        value=None,
        status="unknown",
        confidence_score=0.0,
        interpretation="no mutation pattern corroborated",
        rule="append | update | reducer_shape",
    )


def detect_p3(facts: RepoFacts) -> FieldRecord:
    graphish: list[Observation] = []
    for cls in facts.classes:
        names = set(cls.methods)
        if {"add_node", "add_edge"} <= names or {"add_nodes", "add_edges"} <= names:
            graphish.append(Observation("ast_code_match", f"{cls.name} exposes node and edge builders", cls.location))
    if graphish:
        return FieldRecord(
            field="routing.topology",
            value="directed_graph",
            status="inferred",
            confidence_score=0.7,
            interpretation="control is assembled as nodes plus edges",
            rule="graph_builder = add_node + add_edge",
            observations=graphish,
        )
    return FieldRecord(
        field="routing.topology",
        value=None,
        status="unknown",
        confidence_score=0.0,
        interpretation="no graph or pipeline wiring corroborated",
        rule="graph_builder = add_node + add_edge",
    )


def detect_p4(facts: RepoFacts) -> FieldRecord:
    routers: list[Observation] = []
    for fn in [*facts.functions, *[m for c in facts.classes for m in c.methods.values()]]:
        lower = fn.name.lower()
        if any(tok in lower for tok in ("route", "dispatch", "next_step", "choose", "select")):
            routers.append(Observation("ast_code_match", fn.name, fn.location))
        if fn.returns_name and _hint_hit(fn.name, {"next", "route", "select"}):
            routers.append(Observation("ast_code_match", f"{fn.name} returns a name", fn.location))
    if routers:
        return FieldRecord(
            field="routing.router_type",
            value="conditional_dispatch",
            status="inferred",
            confidence_score=0.55,
            interpretation="a named function appears to select the next target",
            rule="router_name | return_name",
            observations=routers[:5],
        )
    return FieldRecord(
        field="routing.router_type",
        value=None,
        status="unknown",
        confidence_score=0.0,
        interpretation="next-step selection mechanism not corroborated",
        rule="router_name | return_name",
    )


def detect_p5(facts: RepoFacts) -> FieldRecord:
    hits: list[Observation] = []
    for cls in facts.classes:
        methods = set(cls.methods)
        invoke = bool(methods & {"invoke", "run", "call", "__call__"})
        schema = bool(methods & {"schema", "parameters", "model_json_schema", "input_schema"})
        if invoke and schema:
            hits.append(Observation("ast_code_match", f"{cls.name} has invoke/run plus schema", cls.location))
        elif invoke and "tool" in cls.name.lower():
            hits.append(Observation("ast_code_match", f"{cls.name} is an invocable tool-shaped type", cls.location))
    if hits:
        return FieldRecord(
            field="tool_boundary.present",
            value=True,
            status="supported",
            confidence_score=0.74,
            interpretation="a name/schema/invoke capability surface exists",
            rule="tool = (invoke|run|__call__) + (schema|tool-shaped type)",
            observations=hits[:5],
        )
    return FieldRecord(
        field="tool_boundary.present",
        value=None,
        status="unknown",
        confidence_score=0.0,
        interpretation="no capability boundary corroborated",
        rule="tool = (invoke|run|__call__) + (schema|tool-shaped type)",
    )


def detect_p6(facts: RepoFacts) -> FieldRecord:
    protocol_lits = sorted(s for s in facts.string_lits if s in MCP_METHODS or s.lower() in MCP_METHODS)
    sdk = "mcp" in facts.imports
    doc = [p for p in DOC_MCP_PHRASES if p in facts.readme_text.lower()]
    obs: list[Observation] = []
    for lit in protocol_lits:
        obs.append(Observation("string_literal", lit, "repo-wide string literal"))
    if sdk:
        obs.append(Observation("import", "mcp", "import mcp"))
    rejected: list[dict[str, str]] = []
    if doc and not protocol_lits and not sdk:
        rejected.append({
            "channel": "readme_text",
            "claim": ", ".join(doc),
            "reason": "documentation claim without protocol methods or official SDK import",
        })
        return FieldRecord(
            field="mcp_integration.host_location",
            value=None,
            status="unsupported",
            confidence_score=0.22,
            interpretation="MCP is claimed in documentation only",
            rule="P6 requires protocol methods or official mcp SDK, not the word MCP",
            observations=[Observation("readme_text", p, "README.md") for p in doc],
            rejected=rejected,
        )
    if protocol_lits or sdk:
        primitives = {
            "tools": any(x.startswith("tools/") for x in protocol_lits) or sdk,
            "resources": any(x.startswith("resources/") for x in protocol_lits),
            "prompts": any(x.startswith("prompts/") for x in protocol_lits),
        }
        return FieldRecord(
            field="mcp_integration.protocol",
            value={"detected": True, "primitives": primitives, "sdk_import": sdk},
            status="supported",
            confidence_score=0.88 if protocol_lits else 0.7,
            interpretation="capability boundary speaks MCP protocol methods",
            rule="P6 = tools/list|tools/call|resources/*|prompts/* or import mcp",
            observations=obs,
        )
    return FieldRecord(
        field="mcp_integration.host_location",
        value=None,
        status="unknown",
        confidence_score=0.0,
        interpretation="no MCP protocol evidence and no documentation claim",
        rule="P6 = protocol methods or official mcp SDK",
    )


DETECTORS = {
    "P1": detect_p1,
    "P2": detect_p2,
    "P3": detect_p3,
    "P4": detect_p4,
    "P5": detect_p5,
    "P6": detect_p6,
}


def discover(root: Path) -> dict:
    """Run P1-P6. Never consult signature rule tables."""
    facts = collect_facts(root)
    fields = [fn(facts) for fn in DETECTORS.values()]
    return {
        "experiment": "CIR-HOLDOUT-001",
        "condition": "generic",
        "root": str(root),
        "files_scanned": len(facts.files),
        "fields": [f.to_dict() for f in fields],
    }
