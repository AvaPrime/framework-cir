# M1.6-C score

Question: can identity be established from a set when complementary roles are not always write/read-tagged?

Original 9-case corpus unchanged. `bind()` pairwise API unchanged for n!=2. `reconstruct()` not wired. Holdout closed.

## C1 Role discovery

| Pair | Expected | Got |
|---|---|---|
| persist/restore | bound | bound |
| snapshot/hydrate | bound | bound |
| store/load | bound | bound |
| emit/consume | bound | bound |
| serialize/deserialize | bound | bound |
| save/log (same owner) | unbound | unbound |
| create/delete | unbound | unbound |
| send/receive | unbound | unbound |
| append/iterate | unbound | unbound |

9/9. False-bound: 0.

This *is* a closed polarity table (`_PUT` / `_GET`) plus an explicit non-complement list. Recall rose because the table grew, not because roles were inferred from data flow. That limit stays on the record.

## C2 Multi-observation pairing

Bag: `A.write`, `A.read`, `A.inspect`, `B.save`, `B.load`, `Noise.append`.

| Pair | Expected | Got |
|---|---|---|
| A.write ↔ A.read | bound | bound |
| B.save ↔ B.load | bound | bound |
| anything ↔ A.inspect | not bound | not bound |
| anything ↔ Noise.append | not bound | not bound |

False-bound: 0. Unrelated observations did not reinforce.

## Ladder

| Experiment | Score | False-bound |
|---|---|---|
| M1.6-A | 9/9 | 0 |
| M1.6-B | 6/8 | 0 |
| M1.6-C | C1 9/9, C2 2 pairs / 0 false | 0 |

Recall improved on tagged polarity families. Coverage is still not a general theory. Holdout stays closed.
