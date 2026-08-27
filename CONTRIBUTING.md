# Contributing to Framework CIR

Thank you for helping map AI-framework architecture with evidence instead of slogans.

## Ground rules

- Every CIR field you change must have an `evidence_anchors` entry.
- Prefer `ast_code_match` over documentation. Quote a path, class, or function.
- Do not raise confidence above 0.85 without an AST or test-file anchor.
- Pin `entity_metadata.version` and `commit_hash`. Floating `main` is not a catalog entry.
- Schema edits bump `cir_version` and add a note in `docs/SCHEMA.md`.

## Adding a framework

1. Fork and branch from `main` (`feat/cir-<framework>-<version>`).
2. Place the document at `catalog/<framework>_<version>.json`.
3. Validate:

   ```bash
   python -m framework_cir.validate
   ```

4. Update `catalog/COMPARISON.md` with one row per new CIR field you rely on.
5. Open a pull request. Use the catalog template.

## Changing the schema

CIR is an IR. Additive optional fields are preferred. Breaking enum changes require a minor version bump (1.0.2 → 1.1.0).

## Code style

- Python 3.10+, ruff-friendly, no unused imports.
- Tests live in `tests/` and must not require network.

## What we will reject

- Catalog entries sourced only from blog posts or vendor comparison tables.
- Collapsing `mcp_integration` back to a single boolean.
- Mixing two products in one entity (e.g. AutoGen 0.7 + Microsoft Agent Framework 1.0).
