# M1.7 first score

Binder: `bind_structure` — ASSIGN/RETURN of the same target. Method names ignored.

| Case | Expected | Got |
|---|---|---|
| Vault.a / Vault.b on `self.cells[key]` | bound | bound |
| Store.q / Store.z on `self.state` | bound | bound |
| same owner, cells vs log | unbound | unbound |
| two ASSIGNs | insufficient_evidence | insufficient_evidence |
| Vault vs Other, same shape | unbound | unbound |
| methods named save/load, different targets | unbound | unbound |

False-bound: 0. Bound cases used no `_PUT`/`_GET` verb.

Limit: the observation already encodes access direction (`ASSIGN`/`RETURN`). That is less than a verb list, more than raw AST. Next tightening is deriving those labels from assignment vs return nodes, still synthetic.
