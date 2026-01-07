import asyncio
from agent.graph import create_agent


async def run_console_chat():
    agent = create_agent()
    state = {
        "step": "start",
        "user_input": "",
        "response": "",
    }

    while True:
        input("------Press enter to start------")
        result = await agent.ainvoke(state)

        print(f"\nAssistant-> {result.get('response')}")

        if result.get('user_input').lower() in ("exit", "quit"):
            print("Exiting chat.")
            break


if __name__ == "__main__":
    asyncio.run(run_console_chat())
