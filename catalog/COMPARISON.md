# CIR v1.0.2 comparison — LangGraph vs CrewAI vs AutoGen

Analyzed 2026-08-27 from live GitHub heads (not marketing copy).

| CIR field | LangGraph 1.2.11 | CrewAI 1.15.17 | AutoGen 0.7.5 |
|---|---|---|---|
| architecture_model | state_graph | hybrid (vector + hierarchical scope) | message_log |
| context_scope | thread (`thread_id`) | global / hierarchical path | thread |
| persistence_mechanism | sqlite_checkpoint (also postgres) | vector_db (LanceDB default) | ephemeral_ram (ListMemory default) |
| mutation_rule | reducer_merge | time_decay + consolidation | append_only |
| retrieval_trigger | deterministic_pass | semantic_similarity (composite score) | explicit_tool_call |
| determinism_guarantee | full_checkpointed | none_stochastic | none_stochastic |
| epistemic_provenance_support | false | true (`MemoryRecord.source` / `private`) | false |
| topology | cyclic_graph | hierarchical_swarm (default sequential) | event_driven |
| execution_mode | checkpointed_state_machine | sync_blocking (+ native async) | async_event_loop |
| router_type | static_conditional_edge | llm_decision_node (hierarchical manager) | llm_decision_node |
| cycle_recovery | human_in_the_loop_interrupt | none | recursion_limit_exception |
| mcp_native | false (adapters only) | true (`crewai.mcp`) | false |
| mcp.host_location | adapter_package | in_tree | none |
| mcp.agent_dsl_field | tools (bound after get_tools) | mcps | none |
| mcp.primitives | tools + resources + prompts | tools only | none |
| mcp.transports | stdio, streamable_http, sse | stdio, streamable_http, sse | — |
| mcp.tool_filtering | manual | static_and_dynamic | none |
| mcp.session_model | per_call_stateless | long_lived | none |
| mcp.exposes_agent_as_server | true (Agent Server `/mcp`) | false | false |

## Structural inferences (Layer 5 style)

1. **Replay / time-travel.** Only LangGraph compiles to `full_checkpointed` + `deterministic_pass`. CrewAI and AutoGen cannot guarantee identical recovered state across two runs of the same prompt.
2. **Context exhaustion.** AutoGen `append_only` message log is the highest risk of unbounded context growth. LangGraph can overwrite via reducers. CrewAI sidesteps the raw log by retrieving a scored subset from a vector store, at the cost of stochastic recall.
3. **Provenance.** CrewAI is the only one of the three with first-class source/privacy fields on memory records. None of the three implement a full evidence graph (claim → source hash → confidence).
4. **MCP.** Boolean `mcp_native` is too coarse. CrewAI is an in-tree tools-only host with filters. LangGraph uses `langchain-mcp-adapters` and covers tools + prompts + resources, and can expose a graph as an MCP server. AutoGen 0.7.5 has no first-class host.
5. **Naming drift vs CIR.** CrewAI no longer exposes `LongTermMemory` / `EntityMemory` as the primary public types; the live primitive is `Memory` + `MemoryScope`. Any catalog still using the old names is stale.
