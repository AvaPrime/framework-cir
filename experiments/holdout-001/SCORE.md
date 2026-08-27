# Run A score — CIR-HOLDOUT-001

Subject: smolagents 1.26.0 @ `12c1bc8`. Detectors: `freeze/m1-detectors`. Rubric frozen in `RUBRIC.md`. Reference frozen in `REFERENCE.md`.

This is the M1 measurement. Detectors were not edited after scoring.

## Dual-axis table

| Field | Run A | Reference | Axis A | Axis B | Calibration |
|---|---|---|---|---|---|
| P1 persistence | `durable_snapshot` supported 0.86 | `ephemeral_step_log`; not durable | **FP** | scope-confounded | overconfident |
| P2 mutation | `overwrite_merge` inferred 0.58 | `append_only` | **FP** | scope-confounded | mildly overconfident |
| P3 topology | unknown 0.00 | `iterative_step_loop`; not a graph | **TN** for graph; **FN** for step-loop | refusal | well-calibrated *as graph refusal* |
| P4 routing | unknown 0.00 | `llm_action_until_final_answer` | **FN** | refusal | underconfident relative to a recoverable loop |
| P5 tools | present supported 0.74 | present (`Tool`) | **TP** | corroborated (invoke+schema) | well-calibrated |
| P6 MCP | protocol supported 0.70 via `import mcp` | adapter host, tools-only, 3 transports | **TP** (coarse “exists”) / **PARTIAL** vs 1.0.2 block | lexical-only | overconfident |

## Findings (the result)

1. **P1 is the cleanest instrument failure.** Run A pooled `Agent.save` (code export), Gradio uploads, tool file writes, and unrelated `get_*` readers into one durable-snapshot claim. The real memory primitive is an in-process step list. Detection found persistence-*shaped vocabulary*. Derivation did not establish execution-state persistence.

2. **P6 is a TP for the wrong reason.** Smolagents 1.26.0 *does* implement MCP (adapter: `MCPClient` / `ToolCollection.from_mcp`, stdio + streamable-http + sse, tools only). Run A never cited `mcp_client.py`. It cited `import mcp`. Field-level precision hides a derivation-quality failure.

3. **P3 refusal is partly earned.** There is no `add_node`/`add_edge` graph. `unknown` is the correct answer *to the question the detector asked*. The actual topology (iterative step loop) was not in the generic ontology, so this is also a taxonomy gap, not only a miss.

4. **P4 is a miss.** The while-loop + final-answer + max_steps bound is visible in `agents.py` without product names. The detector required a function named route/dispatch/select.

5. **P5 is the only field that is both correct and reasonably derived.**

6. **P2 FP** is the same scope bug as P1: incidental `.update()` calls beat the actual `steps.append`.

## Coarse counts (do not use alone)

- Strict field correctness treating P6 as TP and P3 as TN: TP 2, FP 2, FN 1, TN 1.
- Derivation-aware: only P5 is corroborated; P6 lexical-only; P1/P2 scope-confounded; P3/P4 refusal.

## What this does *not* authorize

- Retuning P1–P6 on smolagents.
- A catalog row for smolagents.
- Run B until this score is accepted as the frozen M1 result.

The bottleneck is derivation discipline (scope + identity + complementary pairs), not the absence of another framework in `/catalog`.
