Assessment Task 2: Refactoring onboarding_api to LangGraph

## Overview
- Migrate the existing custom graph implementation in `onboarding_api/chat_api/agents`
- Adopt the `AgenticGraph` pattern from `langgraph_base`
- Preserve all existing node logic, routing logic, and tools
- Change only graph wiring, state container, and configuration format

## 1. Configuration: routing_config.py → JSON
- Replace `add_conditional_edges` calls with a JSON graph definition
- Define `entry_point`, `nodes`, and `conditional_edges` in `agent_graph.json`
- Map routing outputs (next step values) to node names via `path_map`
- Reuse existing router logic without modification
- Add tool-calling capability by declaring a list of `tools` per node
- Rely on AgenticGraph to normalize `"__end__"` to `END`

## 2. State Management: ConversationState and AgentState
- AgenticGraph operates on AgentState
- Existing nodes expect ConversationState
- Keep ConversationState unchanged
- Use AgentState as the outer runtime state
- Store ConversationState inside AgentState.metadata

### Adapters
- **state_adapter**
  - Extract ConversationState from metadata
  - Execute node logic unchanged
  - Write updated ConversationState back to metadata
  - Return AgentState
- **router_adapter**
  - Extract ConversationState from metadata
  - Call existing `route_by_step` router

## 3. Component Migration: Nodes, Routers, Tools

### Nodes
- Reuse all existing node classes
- Register `node.execute` methods as handlers
- Ensure handler names match JSON configuration

### Routers
- Reuse `route_by_step` unchanged
- Wrap with `router_adapter`
- Register via router registry

### Tools
- Reuse existing tool implementations
- Inject tools during node construction
- Register tools in `tool_registry` for future use (optional)

**Result:**
- All core logic reused
- Only registration and wiring change

## 4. Integration: AgentChatService
- Wrap initial ConversationState into AgentState.metadata
- Invoke agent via `AgenticGraph.workflow`
- Unwrap ConversationState from metadata after execution
- Keep public service API unchanged

## Summary

### Changed
- Graph definition moved to JSON
- State wrapped using adapters
- Nodes registered via handler registry
- Agent built using AgenticGraph

### Unchanged
- Node logic
- Routing logic
- Tool implementations
- Execution logic
- Service interface

# Full migration overview step by step

## Step 1: Update Graph State (ConversationState → AgentState)

### Option 1: Easy route (not recommended)
- Extend agent state instead of replacing it
- Make AgentState inherit ConversationState (may have conflicts)
- Ensure AgentState has the variables required by ConversationState

### Option 2: A bit more involved
- Keep all existing state fields
- Write adapter functions that convert AgentState to ConversationState and vice versa
- Ensure nodes receive ConversationState as input and outputs from nodes are saved in AgentState variables / metadata

## Step 2: Register Nodes as Handlers
- Keep all core node logic unchanged
- AgenticGraph expects a list of handlers, not nodes
- Map all nodes to handlers with proper names

## Step 3: Add State Adapters
- Keep the router function unchanged
- Wrap all node handlers with `state_adapter`
- Wrap router function with `router_adapter`

**Their exact purpose:**
- Extract ConversationState from AgentState
- Execute existing node logic unchanged
- Write updated ConversationState back to metadata
- Return AgentState to the graph

## Step 4: Move Graph Definition to JSON
- Define entry point
- List all nodes
- Define conditional routing
- Map routing outcomes to node names
- Declare end state

## Step 5: Build AgenticGraph Wrapper
- Load graph from JSON config
- Register handlers
- Register routers
- Add tools to `tool_registry`
- Add checkpointer
- Let AgenticGraph compile the workflow

## Step 6: Wrap / Unwrap State in AgentService
- Wrap initial ConversationState into AgentState.metadata
- Invoke agent with AgentState
- Unwrap ConversationState from metadata after execution
- Keep external API compatible with old service

## Step 7: Keep Node and Tool Logic Intact
- Reuse all existing node classes
- Reuse `router_node` and `route_by_step`
- Reuse tool implementations

## Step 8: Deprecate Old Graph Incrementally
- Keep old StateGraph-based implementation intact
- Introduce new agent alongside old one
- Switch service entry point when stable
- Remove old graph once confidence is high
