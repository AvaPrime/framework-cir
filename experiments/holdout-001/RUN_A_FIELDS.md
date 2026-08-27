# Run A field projection (frozen)

Produced by `reconstruct(src/)` with generic detectors only. This is **not** a score.

| Field | Status | Confidence | Value |
|---|---|---|---|
| `memory.persistence_mechanism` | supported | 0.86 | `durable_snapshot` |
| `memory.mutation_rule` | inferred | 0.58 | `overwrite_merge` |
| `routing.topology` | unknown | 0.00 | — |
| `routing.router_type` | unknown | 0.00 | — |
| `tool_boundary.present` | supported | 0.74 | true |
| `mcp_integration.protocol` | supported | 0.70 | detected via `import mcp` |

Graph: 15 observations, 35 relationships (`supports`, `derives`, `corroborates`).

Derivation notes for later scoring (not judgments):

- P1 observations mix `agents.py:save`, Gradio upload save, tool `_write_file`, and unrelated `get_*` readers. Complementary-pair claim is in the output; whether those ops form one architectural pattern is a reference-card question.
- P6 has a single observation (`import mcp`). Detection vs compositional derivation should be scored separately.
- P3/P4 returned `unknown` with zero observations.

Do not retune detectors against these notes.
