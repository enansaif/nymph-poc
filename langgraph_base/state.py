from typing import List, Dict, Any, TypedDict, Optional


class AgentState(TypedDict, total=False):
    """Runtime state shared across LangGraph nodes."""

    conversation_id: str
    user_id: str
    messages: List[Dict[str, Any]]
    step_data: Dict[str, Any]
    next_node: Optional[str]
    chat_state: Optional[str]
    language: Optional[str]
    metadata: Dict[str, Any]
