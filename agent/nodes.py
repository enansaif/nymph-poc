from .state import ConversationState
from .tools import DemoTools


def log_node(node_name, fn):
    def wrapper(state: ConversationState):
        print("\n" + "-" * 50)
        print(f"Executing node: {node_name}")
        print("State BEFORE:")
        print(state)
        new_state = fn(state)
        print("State AFTER:")
        print(new_state)
        print("-" * 50)
        return new_state
    return wrapper


class InitNode:
    def __init__(self, tools: DemoTools):
        self.tools = tools

    def execute(self, state: ConversationState) -> ConversationState:
        state["response"] = "Please provide some input."
        state["step"] = "input"
        return state


class InputNode:
    def __init__(self, tools: DemoTools):
        self.tools = tools

    def execute(self, state: ConversationState) -> ConversationState:
        query = input("\nUser: ")
        state["user_input"] = query
        state["step"] = "process"
        return state


class ProcessNode:
    def __init__(self, tools: DemoTools):
        self.tools = tools

    def execute(self, state: ConversationState) -> ConversationState:
        if not state.get("user_input"):
            state["step"] = "error"
            return state
        result = self.tools.uppercase(state["user_input"])
        state["response"] = result
        state["step"] = "result"
        return state


class ResultNode:
    def __init__(self, tools: DemoTools):
        self.tools = tools

    def execute(self, state: ConversationState) -> ConversationState:
        state["response"] = f"Final result: {state['response']}"
        return state


class ErrorNode:
    def __init__(self, tools: DemoTools):
        self.tools = tools

    def execute(self, state: ConversationState) -> ConversationState:
        state["response"] = "Error: No input provided."
        return state
