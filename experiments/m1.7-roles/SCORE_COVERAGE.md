# M1.7 observation coverage

Measurement of what the extractor can *represent*, not a demand that every construct bind.

| Construct | Represented as | Binds to RETURN self.x? |
|---|---|---|
| `self.x = value` | ASSIGN self.x | bound |
| `self.x += value` | AUG_ASSIGN self.x | insufficient (not collapsed to ASSIGN) |
| `setattr(self, "x", value)` | SETATTR self."x" | insufficient |
| `self.state["x"] = value` | ASSIGN self.state["x"] (ast.Assign) | unbound vs RETURN self.x (different target) |

False-bound: 0. Binder unchanged.

This is coverage, not support. Collapsing += into ASSIGN would hide that it is both read and write.
