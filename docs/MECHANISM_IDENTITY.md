# Mechanism identity (M1.6 contract)

Not implemented in `reconstruct()`. Failure to bind is **unknown**, never `false`.

## Epistemic rule

```
same_mechanism(A, B)
AND complementary_role(A, B)
AND compatible_scope(A, B)
    → corroborates(A, B) is legal
else
    observations remain observations
```

`save()` is not persistence. `import mcp` is not MCP protocol support. A `while` loop is not a router until control semantics and mechanism identity are bound.

## Layer hierarchy

same name ≠ same module ≠ same object ≠ same state ≠ same mechanism

A future binder must report the *highest* layer it can justify, with an evidence basis. Corroboration is legal only at layer `mechanism`.

## Record

See `framework_cir.identity.MechanismIdentity`:

- subject_scope, ownership, execution_context, state_domain
- io_relationship, lifecycle_relationship, temporal_relationship
- evidence_basis, highest_layer

## Independent tests (not the holdout)

`tests/test_identity_contract.py` locks the stub: `bind()` returns `unbound` and `allows_corroboration()` is false. Distinctions a later binder must separate on *synthetic* fixtures, not smolagents:

| Pair | Same verb / name | Same mechanism? |
|---|---|---|
| `Agent.save` exports source vs `Store.save(run_id)` | save | no |
| `import mcp` vs `MCPClient.connect` + transport | mcp | no until bound |
| `dict.update` vs `memory.steps.append` | mutation-shaped | no |
| write(state, id) + read(id) same class | save/load | yes, if scope matches |

Evaluating a future binder against M1 is allowed. Changing M1 is not.
