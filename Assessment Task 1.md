## Architecture Overview

### Onboarding API

#### `chat_router.py`
- Serves as the main API entry point
- Delegates request handling to `AgentChatService`

#### `AgentChatService`
- Wraps the graph-based agent with additional capabilities
- Handles data persistence

#### `agents/graph.py`
- Defines the main graph-based agent
- Attaches and registers all nodes

#### `routing_config.py`
- Defines routing rules for the agent graph
- Controls which nodes are allowed to execute next

#### `state.py`
- Defines the shared `ConversationState` object
- Persists data between node executions

#### `tools.py`
- Defines tools that nodes can use to extend functionality
- Not used in a traditional LLM tool-calling pattern
- Functions as supporting utilities for node logic

#### `nodes/`
- Contains the core business logic of the system
- Each node:
  - Accepts a `ConversationState` as input
  - Executes its specific logic
  - Returns an updated state as output
- Each node sets the `current_node` flag in the state after execution
- The `route_by_step` function uses `current_node` to determine the next node to run

---

### AgentGraph (`langgraph_base`)

#### `config_path`
- Defines the path to a JSON configuration file
- The JSON file acts as the agent blueprint

#### `handlers`
- Used to create and define nodes within the graph
- Each handler represents a single reusable node
- A handler may contain:
  - Multiple database calls
  - One or more LLM invocations
  - Additional internal logic blocks

#### `routers`
- Inspect the current state object
- Decide which node should execute next
- Return the identifier of the next node

#### `tool_registry`
- Dictionary of tools available to the LLM
- Tools can be invoked from any handler

#### `checkpointer`
- Backed by a MongoDB server
- Persists the agent’s current state

#### `AgentState`
- Persistent state object passed to every handler

---

## Summary

### Feasibility
- The `langgraph_base` module aligns well with the onboarding agent’s requirements.
- There is a clear relation between AgentGraph handlers and onboarding agent node classes.
- JSON-based agent declaration is flexible, making it possible to create any graph.
- Tool integration and MongoDB-backed checkpointing support long-running and recoverable conversations.
- Implementation is feasible without requiring major architectural changes.

### Scalability
- Adding new nodes is straightforward due to the handler-based abstraction.
- Routing functions allow control over complex flows.
- A shared persistent state (`AgentState`) enables coordination across new nodes.
- Can easily change agent structure by modifying the JSON config.
- Adding a new node is simple: create a new node class, wrap it with a handler, and update the JSON config.
- Can easily add new tools later in the `tool_registry`.

- Potential challenges as complexity grows:
  - The shared state object may become bloated without a flexible structure.

### Understandability
- Core abstractions (AgentGraph, handlers, routers, state, tools) are logically separated.
- Treating handlers as reusable nodes is intuitive.
- New developers may face a learning curve, especially if unfamiliar with graph-based agents.
- The distinction between `tool_registry` and `research_tools` is a bit confusing.

---

## Recommendations for Improvement

1. **State Management**
   - The `AgentGraph` directly uses `AgentState` to initialize graph state, which isn't flexible.
   - It should go through a level of abstraction; for example, let users create a new state, inherit from `AgentState`, then pass that state to `AgentGraph` Or provide some helper function that does this before initialization.
   - Otherwise, adapter functions are needed to convert `AgentState` to whatever format the nodes expect.
