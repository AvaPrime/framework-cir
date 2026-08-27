# Evidence model

CIR is a **projection** of an evidence graph. It is not where evidence lives.

```
repository
    → observation store
    → P1–P6 analysis passes
    → relationships
    → derivation engine
    → CIR fields
```

Ghidra correspondence (architectural, not an implementation plan):

| Ghidra | Framework CIR |
|---|---|
| Program model | Evidence graph |
| Analyzers | Generic P1–P6 passes |
| P-code | Derived structures (future) |
| FlatProgramAPI | `reconstruct()` / `discover()` |
| Scripts | Informed / Run B consumers |
| XREFs | `supports` `corroborates` `contradicts` `derives` `rejects` |
| Bookmarks | Human reference (not yet stored) |

Relation kinds are defined in `framework_cir.evidence`. Informed priors and human reference must not overwrite generic observations; they coexist and are scored separately in CIR-HOLDOUT-001.

Do not add holdout subjects here. Do not promote documentation into `supported` fields.
