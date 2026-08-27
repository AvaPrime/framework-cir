# Framework CIR

**Canonical Intermediate Representation for AI agent frameworks.**

Framework CIR recovers *structure* from agent frameworks — memory, routing, and MCP integration — and writes it to a versioned, evidence-anchored schema. Marketing names (`Chain`, `Crew`, `Agent`, `Flow`) compile down to the same architectural bytecode so systems can be compared, audited, and tracked over time.

This is Layer 1–3 of a larger reverse-engineering stack (evidence acquisition → structural recovery → CIR). Behavioral reconstruction and evolution diffs are planned; they are not claimed as shipped.

## Why it exists

Agent-framework comparisons are usually feature lists. CIR asks a different question:

> Given this repository, documentation, and commit, what architecture actually shipped?

Every claim carries a source location and a confidence score. AST matches outrank README text.

## Current catalog (CIR v1.0.2)

| Framework | Version | Memory model | Routing | MCP host |
|---|---|---|---|---|
| LangGraph | 1.2.11 | `state_graph` + checkpoint | cyclic state machine | adapter (`langchain-mcp-adapters`) |
| CrewAI | 1.15.17 | hybrid vector + scope | sequential / hierarchical | in-tree (`crewai.mcp`) |
| AutoGen | 0.7.5 | message log | event-driven teams | none in core |

See [`catalog/COMPARISON.md`](catalog/COMPARISON.md) for the full matrix.

## Repository layout

```
schema/                 CIR JSON Schema (versioned)
catalog/                Verified CIR documents
src/framework_cir/      Extractor library
tests/                  Schema + catalog validation
docs/                   Design notes
.github/                Issue / PR templates and CI
```

## Install

```bash
python -m pip install -e ".[dev]"
```

Requires Python 3.10+.

## Usage

```python
from pathlib import Path
from framework_cir import scan_repo, apply_rules, LANGGRAPH_RULES

scan = scan_repo(Path("/path/to/langgraph"))
anchors = apply_rules(scan, LANGGRAPH_RULES)
for a in anchors:
    print(a.confidence_score, a.claim, a.source_location)
```

Validate catalog documents:

```bash
python -m framework_cir.validate
```

## Epistemic rules

1. Deterministic parsers build the skeleton. LLMs may only *label*, never invent anchors.
2. Confidence bands: AST corroboration 0.90–1.0, inferred pattern 0.60–0.85, docs/marketing 0.25–0.50.
3. `mcp_native: boolean` is retained for compatibility. Prefer `mcp_integration.host_location`.
4. Do not back-attribute successor products onto an older CIR entity.

## Status

- [x] CIR schema v1.0.2 (`memory`, `routing`, `mcp_integration`)
- [x] Three verified catalog documents
- [x] Hybrid AST extractor prototype
- [ ] Layer 6 behavioral / stochastic-drift harness
- [ ] Layer 7 version-to-version CIR diffs
- [ ] Layer 8 ecosystem graph

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md). New catalog entries need evidence anchors. Schema changes require a version bump.

## License

MIT. See [LICENSE](LICENSE).
