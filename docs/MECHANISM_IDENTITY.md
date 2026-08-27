# Mechanism identity (post-M1 requirement)

Not implemented in `reconstruct()`. This is the derivation contract that M1 showed is missing.

Do not implement as `better_persistence_detector` or `while_loop_means_routing`. Those would be subject-tuned patches. Implement as a *binding* layer that every future corroboration must pass.

## Why this exists

M1 P1 composed `save(A) + write(B) + read(C)` into durable persistence. Those operations were real. They were not one mechanism. M1 P6 composed `import mcp` into MCP-supported. The import was real. It was not the architecture (`mcpadapt` → `MCPClient` → transports → tools).

## Contract

An edge `corroborates(A, B)` is legal only if all of the following hold:

```
same_mechanism(A, B)
AND complementary_role(A, B)
AND compatible_scope(A, B)
```

Until those predicates are established, A and B remain observations. They must not become an architectural field.

## Binding dimensions

| Dimension | Question |
|---|---|
| Subject identity | Same type / instance family? |
| State identity | Same object being written and later read? |
| Lifecycle | Same run / session / process boundary? |
| Call or data relationship | Does A feed B, or only share a verb? |
| Module / package scope | Same subsystem, or UI vs runtime vs packaging? |
| Storage identity | Same backing medium? |

## Pipeline this implies

```
Observation
    → entity / mechanism identity
    → scope
    → relationship
    → derivation
    → CIR projection
```

`reconstruct()` today lifts FieldRecords into a graph after the fact. That lift is not this layer. Wiring identity into derivation is a later version. Evaluating that version against M1 is allowed. Changing M1 is not.

## Routing, separately

P4's miss is control-flow semantics (condition → iteration → step → termination), not a missing product name. A generic control-flow analyzer is in scope for a later detector *class*. Instantiating it as `while_loop` because smolagents uses a while loop is out of scope until it is specified and tested on fixtures that are not the holdout.
