# CIR-HOLDOUT-001 scoring rubric (frozen before the reference card)

Do not change this document to make Run A look better or worse.

## Ground truth source

Primary: pinned tree `huggingface/smolagents@12c1bc820eca50ace6f80a21d90426d41d74f845` path `src/`.

Documentation may corroborate. It cannot be the sole support for a reference value.

## Field definition (what the analyst must establish)

| ID | Question the reference must answer |
|---|---|
| P1 | Is *execution state* written and later read under a stable identity, with a backing store and resume semantics? File I/O and package export do not count by themselves. |
| P2 | How does agent memory change: append, overwrite, reducer, retrieve+upsert? |
| P3 | How is control wired: graph, pipeline, supervisor tree, event bus, or iterative step loop? |
| P4 | What selects the next action? |
| P5 | Is there a name + schema + invoke capability boundary? |
| P6 | Decompose MCP: host location, tools/resources/prompts, transports, session, agent-as-server. An `import mcp` is not the integration. |

## Axis A — field correctness

Compare Run A *value/status* to the reference value.

| Label | Meaning |
|---|---|
| TP | Run A asserted a value compatible with the reference |
| FP | Run A asserted a value the reference rejects |
| FN | Reference establishes a value; Run A is `unknown` or a different incompatible value |
| TN | Reference cannot establish the field; Run A is `unknown` / `unsupported` |
| PARTIAL | Compatible at a coarse grain, wrong at the CIR grain (record both) |

`unsupported` on a documentation-only claim is TN when the reference also rejects that claim.

## Axis B — derivation quality (independent of correctness)

| Label | Meaning |
|---|---|
| compositional | Multiple complementary observations plus relationships justify the field |
| corroborated | At least two mutually supporting observations of the *same* mechanism |
| direct | One structural observation of the actual mechanism |
| weakly-supported | Observations exist but do not form the claimed mechanism |
| lexical-only | Name, import, or verb fired; protocol/architecture not shown |
| scope-confounded | Observations from unrelated subsystems were pooled |
| refusal | Zero observations, status `unknown` |

A field may be TP and lexical-only at the same time.

## Calibration

| Label | Rule of thumb |
|---|---|
| well-calibrated | Confidence band matches derivation quality and correctness |
| overconfident | High confidence (≥ 0.70) on lexical-only or scope-confounded evidence |
| underconfident | Low confidence despite compositional support |
| n/a | Status `unknown` at 0.00 |

Unknown at 0.00 is well-calibrated *when the reference also cannot place the value in the detector's ontology*, and FN+refusal when the reference value was recoverable by generic means the detector simply missed.
