from typing import TypedDict, Literal


class ConversationState(TypedDict):
    step: Literal["start", "input", "process", "result", "error"]
    user_input: str
    response: str
