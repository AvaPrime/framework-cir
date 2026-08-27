# M1 — Blind Architectural Discovery: closed and measured

Status: **complete**. This document does not change.

Subject: Hugging Face smolagents 1.26.0 @ `12c1bc820eca50ace6f80a21d90426d41d74f845`  
Detectors: `freeze/m1-detectors` @ `13f614143d05b97be4346a60fc4b7f8e80eb3138`  
Rubric / reference / score: `RUBRIC.md`, `REFERENCE.md`, `SCORE.md`

Run B was not performed. Catalog rows were not added. Detectors were not edited after scoring.

## Finding (frozen)

> CIR's generic discovery layer can recover some architectural primitives from an unseen framework, but its current derivation layer confuses local structural signals with architecture-level identity. It is therefore capable of discovery, but not yet reliable architectural reconstruction.

## Checklist

| Item | |
|---|---|
| Representation (M0 / CIR 1.0.2) | done |
| Blind holdout | done |
| No subject-specific tuning | done |
| Reference rubric before scoring | done |
| Field scoring | done |
| Derivation scoring | done |
| Calibration | done |
| Run B | **closed** |

## Known failure modes (negative-control corpus)

Future detector work may be *evaluated* against this list. M1 scores are not a loss function to drive to zero on this subject.

1. **Scope conflation** — P1 pooled code-export `save()`, Gradio uploads, tool file I/O, and unrelated readers into `durable_snapshot`.
2. **Mechanism conflation** — P2 treated incidental `dict.update` as the agent-state mutation model (`steps.append`).
3. **Lexical MCP promotion** — P6 `supported` from `import mcp` while `mcp_client.py` was never cited.
4. **Nameless control-flow miss** — P4 did not recover `while not final_answer and step <= max_steps`.
5. **Insufficient derivation evidence** — corroboration fired without same-mechanism / same-scope binding.

## What M1 authorizes next

Mechanism identity: observations may corroborate only after they are bound to the same subject, state object, lifecycle, and store.

What M1 does **not** authorize: patching `while` → routing against this holdout; raising P1/P6 thresholds on this tree; a smolagents catalog document; Run B.
