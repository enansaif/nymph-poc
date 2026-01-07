from typing import Dict
from langgraph.graph import END
from .state import ConversationState


def router_node(state: ConversationState) -> ConversationState:
    return state


def route_by_step(state: ConversationState) -> str:
    return state["step"]


def get_all_node_names():
    return ["input", "init","process", "result", "error"]


def build_router_edges(end_node=END) -> Dict[str, str]:
    return {
        "start": "init",
        "input": "input",
        "process": "process",
        "result": end_node,
        "error": "error",
    }


def build_node_edges(node_name: str, end_node=END) -> Dict[str, str]:
    edges = {
        "init": {"input": "input"},
        "input": {"process": "process"},
        "process": {"result": "result", "error": "error"},
        "result": {},
        "error": {},
    }
    return edges.get(node_name, {})
