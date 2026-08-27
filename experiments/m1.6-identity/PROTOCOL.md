# M1.6 — Mechanism identity (protocol, frozen)

Subject: synthetic pairs in `tests/fixtures/identity/cases.json` only.
Holdout (smolagents) is out of scope until this protocol is scored.

## Question

> Can a mechanism binder distinguish observations that belong to the same architectural mechanism from observations that merely look semantically related?

## Outcomes (ternary)

| Decision | Justified proposition |
|---|---|
| `bound` | A and B instantiate the same mechanism |
| `unbound` | A and B are distinct mechanisms |
| `insufficient_evidence` | neither proposition is established |

`not proven same` ≠ `proven different`.

A decision is never a CIR field. Binding only licenses corroboration.

## Severity

**False bound is the most serious error.** It is the M1 persistence/MCP failure mode: claiming a mechanism identity that does not exist.

| Error | Meaning | Severity |
|---|---|---|
| False bound | Declared same mechanism; they are not | worst |
| False unbound | Declared distinct; they are the same | serious |
| False insufficient | Refused a pair the corpus marks bound or unbound | milder |
| Missed abstention | Bound or unbound a pair the corpus marks insufficient | serious |

Desired path is not `insufficient → bound` as fast as possible. It is more structural evidence, then identity justified, then bound — or evidence of distinct ownership/scope/state, then unbound.

## Metrics (when a binder exists)

| Dimension | Question |
|---|---|
| Identity precision | Of pairs declared `bound`, how many are corpus-`bound`? |
| Identity recall | Of corpus-`bound` pairs, how many did the binder bind? |
| Negative discrimination | Of corpus-`unbound` pairs, how many stay `unbound`? |
| Abstention | Of corpus-`insufficient_evidence` pairs, how many stay insufficient? |
| Evidence locality | Does the decision cite structural facts, not names? |
| Name invariance | Does renaming identifiers collapse binding? |
| Scope sensitivity | Does crossing object/module/state scope prevent false bound? |

Precision on `bound` outranks recall. A binder that abstains is preferable to one that binds eagerly.

## Sequence

1. Keep `bind()` as `insufficient_evidence` until a binder is specified independently of this holdout.
2. Implement binder against *synthetic* fixtures only.
3. Score this protocol.
4. Freeze that score.
5. Only then evaluate the binder against frozen M1 (no detector edits to chase M1).

Guard invariant (already tested): the stub must not return `bound`.
