import asyncio
from new_graph import create_agent
from adapters import STATE_KEY


def wrap_state(state):
    return {
        "metadata": {
            STATE_KEY: state
        }
    }


def unwrap_state(state):
    metadata = state.get("metadata") or {}
    conversation = metadata.get(STATE_KEY)
    if conversation is None:
        raise RuntimeError("ConversationState missing in metadata")
    return conversation


async def run_console_chat():
    agent = create_agent()

    while True:
        state = {
            "step": "start",
            "user_input": "",
            "response": "",
        }

        input("------Press enter to start------")

        result = await agent.ainvoke(wrap_state(state))
        state = unwrap_state(result)

        print(f"\nAssistant-> {state}")

        if state.get("user_input").lower() in ("exit", "quit"):
            print("Exiting chat.")
            break


if __name__ == "__main__":
    asyncio.run(run_console_chat())
