# Mechanism identity (M1.6 contract)

`bind()` is not wired into `reconstruct()`. It has no authority yet.

## Three outcomes

| Status | Means | Does *not* mean |
|---|---|---|
| `bound` | Same mechanism justified at layer `mechanism` | The CIR field is true |
| `unbound` | Evidence establishes *different* mechanisms | The CIR field is false |
| `insufficient_evidence` | Sameness and difference are both unproven | Negative evidence |

The stub returns `insufficient_evidence` for every pair. Claiming `unbound` without a binder would be a false claim of difference.

Corroboration is legal only when `status == bound` and `highest_layer == mechanism`.

## Binding relation (future)

```
A.state_domain == B.state_domain
A.owner        == B.owner
A.lifecycle    ↔ B.lifecycle
A.role         ⊥ B.role     # complementary, not identical
```

Not: `A.name ≈ B.name`.

Same mechanism under different names (`checkpoint`/`resume` vs `persist`/`restore`) must be bindable. Same verb on different owners must not.

## Synthetic corpus

`tests/fixtures/identity/cases.json` is the measurement set. It is not smolagents, LangGraph, or CrewAI.

A future binder is measured against those expected labels. The stub is measured against *not implementing them*.
