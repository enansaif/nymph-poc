from langgraph_base.base_graph import AgenticGraph

from agent.nodes import (
    InitNode,
    InputNode,
    ProcessNode,
    ResultNode,
    ErrorNode,
    log_node,
)
from agent.router import router_node, route_by_step
from agent.tools import create_demo_tools


class DemoAgentGraph(AgenticGraph):
    def __init__(self):
        tools = create_demo_tools()

        handlers = {
            "router": log_node("router", router_node),
            "init": log_node("init", InitNode(tools).execute),
            "input": log_node("input", InputNode(tools).execute),
            "process": log_node("process", ProcessNode(tools).execute),
            "result": log_node("result", ResultNode(tools).execute),
            "error": log_node("error", ErrorNode(tools).execute),
        }

        routers = {
            "route_by_step": route_by_step
        }

        super().__init__(
            config_path="agent_graph.json",
            handlers=handlers,
            routers=routers,
            checkpointer=None,
            tool_registry=tools
        )


def create_agent():
    return DemoAgentGraph().workflow
