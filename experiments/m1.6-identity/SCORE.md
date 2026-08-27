# M1.6 first binder — score

Binder: `framework_cir.identity.bind` (owner + complementary role + scope).
Corpus: `tests/fixtures/identity/cases.json` (9 pairs).
Not applied to smolagents. Not wired into `reconstruct()`.

## Results

| Case | Expected | Binder |
|---|---|---|
| same-object-save-restore | bound | bound |
| same-state-write-read | bound | bound |
| mcp-list-and-call-same-session | bound | bound |
| same-mechanism-different-names | bound | bound |
| agent-export-vs-config-save | unbound | unbound |
| unrelated-appends | unbound | unbound |
| import-mcp-vs-ordinary-tool | unbound | unbound |
| readme-vs-unrelated-impl | unbound | unbound |
| lone-save | insufficient_evidence | insufficient_evidence |

9/9 on this corpus.

## What this does **not** show

- Vocabulary independence beyond the role pairs in `_COMPLEMENTS` (persist/restore, put/get, checkpoint/resume, tools/list+call). A pair that is complementary in structure but uses unlisted verbs stays `insufficient_evidence`.
- Type-level or data-flow identity. Owner is parsed from `file:Class.method` in the synthetic locations.
- Repair of frozen M1. That evaluation is a later measurement.

## Errors on this run

None on the nine cases. False-bound count: 0. That is the metric that matters; it is not a license to reopen the holdout.
