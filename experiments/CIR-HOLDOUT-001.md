# CIR-HOLDOUT-001

Held-out architectural reconstruction benchmark.

This experiment measures whether Framework CIR can recover architecture from **first principles**, not whether we already know the framework.

Baseline freeze: branch `freeze/cir-1.0.2` (commit of the signature-based prototype + three catalog documents). Do not add framework-specific rule-table entries until Run A is frozen.

## Success criterion

Not: "CIR successfully reconstructed framework X."

Yes:

> Given a previously unseen AI framework, CIR can recover a measurable subset of its architecture using generic structural evidence, distinguish observation from inference, calibrate uncertainty, and produce a provenance-complete representation.

## Contamination rules

A subject is **ineligible** if any of the following is true before Run A is frozen:

- It already has a rule table (`LANGGRAPH_RULES`, `CREWAI_RULES`, `AUTOGEN_RULES`).
- A CIR catalog document already exists for it.
- Framework-specific signatures are added to the extractor during the blind pass.

Human prior knowledge of the framework is unavoidable. It may be used only to write the **reference analysis after Run A is frozen**. It may not steer detectors mid-run.

LangGraph, CrewAI, and AutoGen are **training / calibration subjects**, not holdouts.

## Two runs

### Run A — blind

Inputs: held-out repository at a pinned commit, generic detectors only, CIR schema (1.0.2 fields + derivation records if 1.1 instrumentation is merged *before* A), documentation as a separate evidence channel.

Output: `experiments/holdout-001/run-a.cir.json` plus a derivation log.

Freeze that artifact. No edits after freeze except typo/schema-validation fixes that do not change field values.

### Run B — informed

After freeze: framework-specific signatures may be added.

Output: `experiments/holdout-001/run-b.cir.json`.

The scientifically useful object is the **delta**:

```
generic recovery  →  informed enhancement  →  what required prior knowledge?
```

## Recovered primitives (small ontology)

Do not look for author names. Look for behavior.

| ID | Question | Positive evidence (examples) | CIR-facing output |
|---|---|---|---|
| P1 Persistence | Is execution state written and later read under an identity? | serialize/save/load, snapshot objects, DB writes, resume paths | `memory.persistence_mechanism`, `determinism_guarantee` |
| P2 Mutation | How does state change? | overwrite, append, reducer(old, delta), event emit, retrieve+upsert | `memory.mutation_rule` |
| P3 Topology | How is control wired? | graph builders, pipelines, supervisor, event bus, queue, recursion, fan-in/out, cycles | `routing.topology`, `execution_mode` |
| P4 Routing | What decides the next step? | static edges, conditionals, tool choice, supervisor choice, subscriptions, human gate, LLM next-action | `routing.router_type`, `cycle_recovery_mechanism` |
| P5 Tool boundary | How does the model obtain executable capabilities? | registry, name+schema+invoke+result | tool surface (pre-MCP) |
| P6 MCP shape | Is that boundary MCP-protocol-shaped? | transports, list/call, resources, prompts, session | `mcp_integration.*` |

MCP is a **second question**. First recover a tool boundary. Then ask whether it implements recognizable MCP semantics. String match on `"MCP"` is documentation evidence, not protocol evidence.

### MCP blind cases (must be scored)

| Case | Docs | Source | Expected CIR |
|---|---|---|---|
| A | "native MCP" | no protocol, no dependency, no transport | `host_location=none`; doc claim retained, not promoted |
| B | little or no MCP branding | protocol implementation present | MCP detected from structure |
| C | MCP mentioned | import of an adapter package | `host_location=adapter_package` |
| D | generic tools vaguely MCP-like | insufficient protocol evidence | uncertain; do not force a boolean |

## Metrics

Against a human reference analysis written **after** Run A freeze:

| Metric | Question |
|---|---|
| Recall | Which reference primitives did CIR miss? |
| Precision | Which CIR claims were not in the reference / not supported? |
| Calibration | Do confidence bands match correctness? |
| Provenance | Can every accepted field be traced observation → interpretation → derivation → field? |

Classify each field:

`TRUE_POSITIVE` · `FALSE_POSITIVE` · `TRUE_NEGATIVE` · `FALSE_NEGATIVE` · `OVERCONFIDENT` · `UNDERCONFIDENT` · `UNSUPPORTED`

Prefer `UNSUPPORTED` / "I don't know" over a fluent wrong architecture.

## Subject selection (not yet pinned)

Holdout must be Python for CIR-HOLDOUT-001 because the extractor is Python-AST-only. A non-Python subject is CIR-HOLDOUT-002 (language generality).

Candidate pool (none selected until freeze of protocol + detectors):

- PydanticAI
- OpenAI Agents SDK (`openai/openai-agents-python`)
- Google ADK
- LlamaIndex agent/workflow packages
- Semantic Kernel Python
- Hugging Face smolagents
- Letta

Selection criterion: public source, pinned release, enough code that persistence/routing/tools can exist, **no existing CIR rule table**.

## What this experiment is not

- Not a fourth catalog row.
- Not a demo that we can reconstruct a framework we already studied.
- Not permission to expand `LANGGRAPH_RULES` until Run A is frozen.
