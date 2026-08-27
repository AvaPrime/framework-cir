# Reference card — smolagents 1.26.0 @ 12c1bc8

Analyst evidence from `src/` at the pinned commit. Docs used only as corroboration.

## P1 Execution-state persistence

**Reference value:** `ephemeral_step_log` (in-process `AgentMemory.steps`). Not `durable_snapshot`.

**Definition used:** write + read + identity + backing store + resume of *run state*.

**Source evidence:**

- `src/smolagents/memory.py` — `AgentMemory` holds `self.steps: list[...]`. `reset()` clears the list. `replay()` pretty-prints to a logger; it does not load a checkpoint.
- `src/smolagents/agents.py:343` — `self.memory = AgentMemory(...)`.
- `src/smolagents/agents.py:488,567,602` — steps are appended during `_run_stream`.
- `src/smolagents/agents.py:892` — `MultiStepAgent.save(output_dir)` exports *agent source* (`tools/`, `agent.json`, `prompt.yaml`, `app.py`). Packaging, not run-state persistence.

**Excluded evidence:** Gradio upload writes, tool `_write_file`, `get_*` helpers, README "Memory" flowchart. Those are not execution checkpoints.

**Rationale:** Memory is an in-process append-only step log. Replay is logging. `save()` is code export. No identity-keyed load of a prior run.

## P2 Mutation

**Reference value:** `append_only` on `AgentMemory.steps`.

**Source evidence:** `self.memory.steps.append(...)` in `agents.py` (task, planning, action, final steps).

**Excluded evidence:** `dict.update` in the Python executor, type-hint parser, and model kwargs assembly.

## P3 Topology

**Reference value:** `iterative_step_loop` (optional `managed_agents` subtree). Not a compiled directed graph.

**Source evidence:** `MultiStepAgent._run_stream` — `while not returned_final_answer and self.step_number <= max_steps`. Classes `CodeAgent` and `ToolCallingAgent` share that loop. No `add_node` / `add_edge` builder.

**Excluded evidence:** README mermaid diagram (docs only).

## P4 Routing

**Reference value:** `llm_action_until_final_answer` bounded by `max_steps` / interrupt.

**Source evidence:** loop continues unless the action step produces a final answer or `max_steps` / `interrupt_switch` fires (`agents.py` `_run_stream`). Tool vs code path is subclass behavior (`ToolCallingAgent` vs `CodeAgent`), still LLM-selected actions.

**Excluded evidence:** functions named `route` / `dispatch` (none required).

## P5 Tool boundary

**Reference value:** present. `Tool` has `name`, `inputs` / JSON schema, `forward`, `__call__` (`tools.py`).

## P6 MCP (decomposed)

| Subfield | Reference | Evidence |
|---|---|---|
| Host location | `adapter_package` | `mcp_client.py` wraps `mcpadapt.core.MCPAdapt` + `SmolAgentsAdapter`; extra `smolagents[mcp]` pulls `mcp` + `mcpadapt` (`pyproject.toml`) |
| Agent DSL field | tools list after `get_tools()` / `ToolCollection.from_mcp` | not a native `Agent.mcps` field |
| Tools | yes | `MCPClient.get_tools()`, `ToolCollection.from_mcp` |
| Resources | no in this tree | no resource helpers in `mcp_client.py` |
| Prompts | no in this tree | same |
| Transports | stdio, streamable-http, sse | `mcp_client.py` docstring + transport check |
| Session | long-lived context manager | `connect` / `disconnect` / `__enter__` |
| Agent as MCP server | false | no `/mcp` server in package |
| list_changed | false (comment says future) | `get_tools` docstring |

**Excluded evidence:** README sentence “Tool-agnostic: MCP server” as sole proof. `import mcp` under `TYPE_CHECKING` in `tools.py`.
