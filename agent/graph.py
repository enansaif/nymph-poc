from langgraph.graph import StateGraph, END
from .state import ConversationState
from .tools import create_demo_tools
from .nodes import (
    InitNode,
    InputNode,
    ProcessNode,
    ResultNode,
    ErrorNode,
    log_node,
)
from .router import (
    router_node,
    route_by_step,
    build_router_edges,
    build_node_edges,
    get_all_node_names,
)


def create_conversation_graph():
    tools = create_demo_tools()

    NODE_CLASSES = {
        "init": InitNode,
        "input": InputNode,
        "process": ProcessNode,
        "result": ResultNode,
        "error": ErrorNode,
    }

    node_instances = {
        name: cls(tools) for name, cls in NODE_CLASSES.items()
    }

    workflow = StateGraph(ConversationState)

    workflow.add_node("router", log_node("router", router_node))

    for name, instance in node_instances.items():
        workflow.add_node(name, log_node(name, instance.execute))

    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
        "router",
        route_by_step,
        build_router_edges(END),
    )

    for node_name in get_all_node_names():
        edges = build_node_edges(node_name, END)
        if edges:
            workflow.add_conditional_edges(
                node_name,
                route_by_step,
                edges,
            )

    return workflow.compile()


def create_agent():
    return create_conversation_graph()
