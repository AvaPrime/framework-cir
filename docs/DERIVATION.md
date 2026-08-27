# Derivation model (CIR 1.1 draft)

Status: specified for CIR-HOLDOUT-001 instrumentation. Not yet the published schema const (`cir_version` remains `1.0.2` on catalog documents).

Current anchors record *where something was seen*. Reconstruction needs *why a field was asserted*.

```
OBSERVATION  →  INTERPRETATION  →  DERIVATION  →  CIR FIELD
```

## Record shape

```json
{
  "field": "memory.persistence_mechanism",
  "value": "checkpointed",
  "confidence_score": 0.94,
  "status": "asserted",
  "derivation": {
    "observations": [
      {
        "kind": "ast_call",
        "symbol": "save_checkpoint",
        "source_location": "src/runtime/checkpoint.py:143"
      },
      {
        "kind": "ast_call",
        "symbol": "load_checkpoint",
        "source_location": "src/runtime/checkpoint.py:188"
      }
    ],
    "interpretation": "execution state is written and later read",
    "rule": "durable_snapshot = save + load + identity_key",
    "evidence_channels": ["ast_code_match"],
    "rejected_channels": [
      {
        "channel": "readme_text",
        "claim": "native persistent memory",
        "reason": "no matching write/read pair in source"
      }
    ]
  }
}
```

`status` is one of: `observed`, `asserted`, `unsupported`, `contradicted`.

Documentation may appear in `observations` with its own channel. It must not be the sole support for `status=asserted` on a structural field.
