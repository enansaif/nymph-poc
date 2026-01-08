from langgraph_base.state import AgentState

STATE_KEY = "conversation"

def state_adapter(node_fn):

    def wrapper(agent_state: AgentState) -> AgentState:
        metadata = agent_state.setdefault("metadata", {})

        conversation_state = metadata.get(STATE_KEY)
        if conversation_state is None:
            raise RuntimeError("ConversationState missing in metadata")

        updated_state = node_fn(conversation_state)
        metadata[STATE_KEY] = updated_state

        return agent_state

    return wrapper

def router_adapter(router_fn):

    def wrapper(agent_state: AgentState) -> str:
        metadata = agent_state.get("metadata") or {}
        conversation_state = metadata.get(STATE_KEY)

        if conversation_state is None:
            raise RuntimeError("ConversationState missing in metadata")

        return router_fn(conversation_state)

    return wrapper

