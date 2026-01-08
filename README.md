LangGraph Agent Console Demo

The agent runs in the terminal and processes simple user input through a small state machine.

WHAT THIS DEMO DOES
---

- Runs a console-based conversational agent
- Uses LangGraph as the execution engine
- Defines the agent workflow in JSON
- Preserves existing node, router, and tool logic
- Demonstrates state adaptation between:
  - ConversationState (business logic)
  - AgentState (LangGraph runtime)

No LLMs or API keys are required.

REQUIREMENTS
---

Python:
- Python 3.9 or higher

Dependencies:
- langchain
- langgraph

Install dependencies with:

pip install langchain langgraph

HOW TO EXECUTE
---

1. Open a terminal in the extracted directory
2. Run the LangGraph-based agent:

For Refactored agent: `python new_agent_service.py`
For Original agent: `python old_agent_service.py`

WHAT TO EXPECT WHEN RUNNING
---

- The program waits for you to press Enter
- A conversation state is initialized
- The agent progresses through nodes based on routing logic
- Each node logs:
  - Node name
  - State before execution
  - State after execution

Execution flow:

router → init → input → process → result/error

Routing is controlled by the "step" field in the state.

EXAMPLE RUNS (`new_agent_service.py`)
---

```--------------------------------------------------
Example 1: Input = "Hello World"
--------------------------------------------------

------Press enter to start------

--------------------------------------------------
Executing node: router
State BEFORE:
{'metadata': {'conversation': {'step': 'start', 'user_input': '', 'response': ''}}}
State AFTER:
{'metadata': {'conversation': {'step': 'start', 'user_input': '', 'response': ''}}}
--------------------------------------------------

--------------------------------------------------
Executing node: init
State BEFORE:
{'metadata': {'conversation': {'step': 'start', 'user_input': '', 'response': ''}}}
State AFTER:
{'metadata': {'conversation': {'step': 'input', 'user_input': '', 'response': 'Please provide some input.'}}}
--------------------------------------------------

--------------------------------------------------
Executing node: input
State BEFORE:
{'metadata': {'conversation': {'step': 'input', 'user_input': '', 'response': 'Please provide some input.'}}}

User: Hello World
State AFTER:
{'metadata': {'conversation': {'step': 'process', 'user_input': 'Hello World', 'response': 'Please provide some input.'}}}
--------------------------------------------------

--------------------------------------------------
Executing node: process
State BEFORE:
{'metadata': {'conversation': {'step': 'process', 'user_input': 'Hello World', 'response': 'Please provide some input.'}}}
State AFTER:
{'metadata': {'conversation': {'step': 'result', 'user_input': 'Hello World', 'response': 'HELLO WORLD'}}}
--------------------------------------------------

--------------------------------------------------
Executing node: result
State BEFORE:
{'metadata': {'conversation': {'step': 'result', 'user_input': 'Hello World', 'response': 'HELLO WORLD'}}}
State AFTER:
{'metadata': {'conversation': {'step': 'result', 'user_input': 'Hello World', 'response': 'Final result: HELLO WORLD'}}}
--------------------------------------------------

Assistant-> {'step': 'result', 'user_input': 'Hello World', 'response': 'Final result: HELLO WORLD'}```

Behavior:
- User input is converted to uppercase
- Final response is returned
- Execution completes

```--------------------------------------------------
Example 2: Input = (blank)
--------------------------------------------------

User:
State AFTER:
{'metadata': {'conversation': {'step': 'process', 'user_input': '', 'response': 'Please provide some input.'}}}
--------------------------------------------------

--------------------------------------------------
Executing node: process
State BEFORE:
{'metadata': {'conversation': {'step': 'process', 'user_input': '', 'response': 'Please provide some input.'}}}
State AFTER:
{'metadata': {'conversation': {'step': 'error', 'user_input': '', 'response': 'Please provide some input.'}}}
--------------------------------------------------

--------------------------------------------------
Executing node: error
State BEFORE:
{'metadata': {'conversation': {'step': 'error', 'user_input': '', 'response': 'Please provide some input.'}}}
State AFTER:
{'metadata': {'conversation': {'step': 'error', 'user_input': '', 'response': 'Error: No input provided.'}}}
--------------------------------------------------

Assistant-> {'step': 'error', 'user_input': '', 'response': 'Error: No input provided.'}```

Behavior:
- Blank input triggers the error node
- An error message is returned

```--------------------------------------------------
Example 3: Input = "exit"
--------------------------------------------------

User: exit

Assistant-> {'step': 'result', 'user_input': 'exit', 'response': 'Final result: EXIT'}
Exiting chat.```

Behavior:
- Input is processed normally
- Program exits after printing the response

KEY IMPLEMENTATION NOTES
---

STATE HANDLING

ConversationState:
- Used by node logic
- Contains:
  - step
  - user_input
  - response

AgentState:
- Required by AgenticGraph
- Wraps ConversationState inside metadata

Example:

{
  "metadata": {
    "conversation": ConversationState
  }
}

--------------------------------------------------------------------

ADAPTERS

Adapters allow existing logic to run unchanged:

- state_adapter
  - Extracts ConversationState
  - Executes node logic
  - Writes updated state back into AgentState

- router_adapter
  - Extracts ConversationState
  - Calls existing routing logic

--------------------------------------------------------------------

JSON-BASED WORKFLOW

The agent structure is defined in agent_graph.json and includes:
- Entry point
- Nodes
- Conditional routing
- Transition mapping

No graph wiring logic is hardcoded.

SUMMARY
---

- Fully runnable from the terminal
- No external services required
- Demonstrates LangGraph with declarative configuration
- Existing logic reused without modification
