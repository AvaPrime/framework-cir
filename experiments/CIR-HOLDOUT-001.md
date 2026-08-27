# CIR-HOLDOUT-001

Held-out architectural reconstruction benchmark.

This experiment measures **discovery capability**, not framework recognition capability.

- Control condition: CIR 1.0.2 signature tables (`LANGGRAPH_RULES`, `CREWAI_RULES`, `AUTOGEN_RULES`) on branch `freeze/cir-1.0.2`.
- Experimental condition: generic detectors P1–P6 in `framework_cir.generic.discover`.

Do not add framework-specific rule-table entries until Run A is frozen.
Do not retune generic detector thresholds after a holdout is selected or after Run A is seen.

## Status vocabulary

Absence of evidence is not evidence of absence.

| Status | Meaning |
|---|---|
| `observed` | A raw fact was seen (call, import, docstring, README phrase) |
| `inferred` | A candidate structure exists; corroboration is incomplete |
| `supported` | Observations justify the CIR field |
| `unsupported` | A claim exists (usually docs) that source does not corroborate |
| `unknown` | No claim and no structural evidence |
| `contradicted` | Channels disagree in a way the field cannot absorb |

`mcp: false` is not the default for "we didn't find it." Use `unsupported` or `unknown`.

## Pipeline

```
CIR 1.0.2 SIGNATURE ERA
        freeze
Generic detector development   (no subject, no catalog row)
        DETECTOR FREEZE on synthetic fixtures only
Select holdout → pin commit → Run A → freeze output
Reference card → score Run A → Run B → score the delta
```

## Success criterion

Not: "CIR successfully reconstructed framework X."

Yes:

> Given a previously unseen AI framework, CIR can recover a measurable subset of its architecture using generic structural evidence, distinguish observation from inference, calibrate uncertainty, and produce a provenance-complete representation.

## Contamination rules

A subject is **ineligible** if any of the following is true before Run A is frozen:

- It already has a rule table (`LANGGRAPH_RULES`, `CREWAI_RULES`, `AUTOGEN_RULES`).
- A CIR catalog document already exists for it.
- Framework-specific signatures are added to the extractor during the blind pass.
- Generic detector thresholds are changed after the subject is chosen.

Human prior knowledge of the framework may be used only to write the **reference analysis after Run A is frozen**.

LangGraph, CrewAI, and AutoGen are **control / calibration subjects**, not holdouts.

## Two runs

### Run A — blind (experimental)

`discover(root)` only. Output: `experiments/holdout-001/run-a.cir.json`.

### Run B — informed (control enhancement)

Framework-specific signatures permitted. Output: `experiments/holdout-001/run-b.cir.json`.

The result that matters is the **delta**: how much architecture was recoverable without priors.

## Recovered primitives

| ID | Question | CIR-facing output |
|---|---|---|
| P1 Persistence | Is execution state written and later read under an identity? | `memory.persistence_mechanism` |
| P2 Mutation | How is state mutated? | `memory.mutation_rule` |
| P3 Topology | How is control wired? | `routing.topology` |
| P4 Routing | What selects the next target? | `routing.router_type` |
| P5 Tool boundary | How does the model obtain capabilities? | `tool_boundary.present` |
| P6 MCP | Is that boundary protocol-shaped? | `mcp_integration.*` |

P6 depends on P5's surface plus protocol methods (`tools/list`, `tools/call`, …) or the official `mcp` SDK import. The word "MCP" in a README is documentation evidence only.

### MCP scoring cases

| Case | Docs | Source | Expected status |
|---|---|---|---|
| A | native MCP | no protocol | `unsupported` |
| B | silent | protocol methods present | `supported` |
| C | MCP mentioned | adapter import only | later Run B / `inferred` adapter |
| D | vague tools | insufficient protocol | `unknown` or `inferred`, never a confident boolean |

## Metrics

Field-by-field against a post-A reference card: recall, precision, calibration, provenance.

Labels: `TRUE_POSITIVE` `FALSE_POSITIVE` `TRUE_NEGATIVE` `FALSE_NEGATIVE` `OVERCONFIDENT` `UNDERCONFIDENT` `UNSUPPORTED`.

## Subject selection (not pinned)

Python-only for 001. Candidate pool remains unchosen until this detector set is treated as frozen:

PydanticAI · OpenAI Agents SDK · Google ADK · LlamaIndex agents · Semantic Kernel Python · smolagents · Letta

## What this experiment is not

- Not a fourth catalog row.
- Not permission to expand signature tables until Run A is frozen and scored.
- Not permission to retune P1–P6 after seeing the holdout.
