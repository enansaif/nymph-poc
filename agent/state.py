from typing import TypedDict


class ConversationState(TypedDict):
    step: str
    user_input: str
    response: str
