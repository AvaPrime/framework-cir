# Thesis

> Framework CIR investigates whether heterogeneous public software artifacts can be transformed into reliable architectural reconstruction when observations are bound to mechanisms independently of product vocabulary.

That is the falsifiable core.

## Pipeline (no skip)

```
Evidence → Observation → Mechanism identity → Corroboration → Derivation → CIR projection
```

No inference step may skip identity.

## Inequalities (invariants)

```
uncertain observation  ≠  negative architectural claim
related observations   ≠  same mechanism
same mechanism         ≠  architectural truth
architectural truth    ≠  decision
```

CIR observes, relates, derives, and represents. Consumers (catalog, Codessa) may decide. CIR does not.

## Ladder

| Step | Question | Result |
|---|---|---|
| M0 | Can we represent architecture? | Yes (CIR 1.0.2) |
| M1 | Can generic discovery find signals in an unseen system? | Yes; local signals are insufficient for derivation |
| M1.6 | Does mechanism identity supply the missing constraint? | Not measured |

M1.6 failure modes that would still be informative: high false-bound (too permissive); excessive abstention (too conservative); binding only when names align (vocabulary not eliminated). Success is binding across renames while rejecting related-but-distinct mechanisms.

M1 is historical. A later binder may beat those frozen errors; it does not erase them. Smolagents is reopened only after the synthetic corpus is scored.

Asymmetric loss: false bound is worse than `insufficient_evidence`. Abstention is legitimate.

Next artifact: a binder that survives `tests/fixtures/identity/cases.json` without product vocabulary — then measurement. Not another feature.
