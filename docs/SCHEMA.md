# CIR schema notes

Current version: **1.0.2** (`schema/cir.schema.json`).

## Required top-level fields

- `cir_version`
- `entity_metadata` (`name`, `version`, `commit_hash`, `source_url`)
- `memory_primitive`
- `routing_primitive`
- `mcp_integration`
- `evidence_anchors`

## mcp_integration (added in 1.0.2)

Replaces overloading `routing_primitive.mcp_native`.

| Field | Meaning |
|---|---|
| `host_location` | Where the MCP client lives |
| `agent_dsl_field` | Framework field that binds servers |
| `primitives` | tools / resources / prompts coverage |
| `transports` | stdio, streamable_http, sse, hosted |
| `tool_filtering` | none, manual, static, static_and_dynamic |
| `session_model` | none, per_call_stateless, long_lived, provider_hosted |
| `exposes_agent_as_server` | Can the agent itself speak MCP as a server? |
| `list_changed_subscriptions` | tools/list_changed (or equivalent) support |

`routing_primitive.mcp_native` remains for compatibility. Treat `mcp_integration.host_location != "none"` as the source of truth.
