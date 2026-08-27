# M1.7-next — AST → Observation

Extractor: `ast_access.extract_access` (assignment / return nodes only).
Binder: frozen `bind_structure`.

| Source | Extractor | Binder |
|---|---|---|
| Vault.a / Vault.b | ASSIGN/RETURN `self.cells[key]` | bound |
| Store.q / Store.z | ASSIGN/RETURN `self.state` | bound |
| Vault cells vs log | ASSIGN cells, RETURN log | unbound |

False-bound: 0. No `_PUT`/`_GET`. Method names appear only in `source_location`.

Limit: only top-level class methods; only `Assign` and `Return`; targets compared as unparsed strings. AugAssign / attribute-set via `setattr` are not covered.
