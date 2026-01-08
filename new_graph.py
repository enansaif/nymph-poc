from langgraph_base.base_graph import AgenticGraph
from adapters import state_adapter, router_adapter

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

        nodes = {
            "router": router_node,
            "init": InitNode(tools).execute,
            "input": InputNode(tools).execute,
            "process": ProcessNode(tools).execute,
            "result": ResultNode(tools).execute,
            "error": ErrorNode(tools).execute,
        }

        handlers = {}

        handlers = {}

        for name, fn in nodes.items():
            if name == "router":
                handlers[name] = log_node(name, fn)
            else:
                handlers[name] = log_node(name, state_adapter(fn))


        routers = {
            "route_by_step": router_adapter(route_by_step)
        }

        super().__init__(
            config_path="agent_graph.json",
            handlers=handlers,
            routers=routers,
            checkpointer=None,
        )


def create_agent():
    return DemoAgentGraph().workflow
