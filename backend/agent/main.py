"""
Personal AI Agent
=================

Entry point for the LangGraph personal AI agent.

Architecture:

User
 ↓
LangGraph
 ↓
Qwen 2.5 14B
 ↓
RAG / GitHub Tools
 ↓
PostgreSQL Checkpointer
 ↓
Persistent Conversation
"""

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
)

from backend.agent.graph import graph


# ============================================================
# DEFAULT SESSION
# ============================================================

DEFAULT_THREAD_ID = "amine-session-001"


# ============================================================
# ASK AGENT
# ============================================================

def ask_agent(
    question: str,
    thread_id: str,
):
    """
    Send a question to the LangGraph agent.

    The thread_id identifies the conversation.
    PostgreSQL uses it to restore previous state.
    """

    if not thread_id or not thread_id.strip():
        thread_id = DEFAULT_THREAD_ID

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=question.strip()
                )
            ]
        },
        config=config,
    )

    return result


# ============================================================
# GET FINAL ANSWER
# ============================================================

def get_final_answer(result) -> str:
    """
    Extract the last textual AI response.
    """

    messages = result.get("messages", [])

    if not messages:
        return "No response was generated."

    for message in reversed(messages):

        if isinstance(message, AIMessage):

            content = message.content

            if isinstance(content, str):

                content = content.strip()

                if content:
                    return content

    return "The agent did not generate a final answer."


# ============================================================
# DEBUG TOOL CALLS
# ============================================================

def print_tool_calls(result):
    """
    Display all tools called during the request.
    """

    messages = result.get("messages", [])

    tool_calls_found = False

    for message in messages:

        # ----------------------------------------------------
        # AI tool calls
        # ----------------------------------------------------

        if isinstance(message, AIMessage):

            tool_calls = getattr(
                message,
                "tool_calls",
                [],
            )

            if tool_calls:

                tool_calls_found = True

                for call in tool_calls:

                    print(
                        f"\n[Tool Call] {call.get('name')}"
                    )

                    print(
                        f"[Arguments] {call.get('args')}"
                    )

        # ----------------------------------------------------
        # Tool results
        # ----------------------------------------------------

        elif isinstance(message, ToolMessage):

            tool_calls_found = True

            print(
                f"\n[Tool Result] {message.name}"
            )

    return tool_calls_found


# ============================================================
# MAIN TERMINAL
# ============================================================

def main():

    print("=" * 80)
    print("PERSONAL AI AGENT")
    print("=" * 80)

    thread_id = DEFAULT_THREAD_ID

    print(
        f"\nThread ID: {thread_id}"
    )

    print("Memory: PostgreSQL")

    print("\nCommands:")
    print("  /new  → start a new conversation")
    print("  /exit → quit")

    while True:

        try:

            question = input("\nYou: ").strip()

        except (
            KeyboardInterrupt,
            EOFError,
        ):

            print("\nGoodbye!")
            break

        if not question:
            continue

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if question.lower() in {
            "/exit",
            "/quit",
            "exit",
            "quit",
        }:

            print("\nGoodbye!")
            break

        # ----------------------------------------------------
        # NEW CONVERSATION
        # ----------------------------------------------------

        if question.lower() == "/new":

            import uuid

            thread_id = (
                f"amine-{uuid.uuid4()}"
            )

            print(
                "\nNew conversation started."
            )

            print(
                f"Thread ID: {thread_id}"
            )

            continue

        # ----------------------------------------------------
        # RUN AGENT
        # ----------------------------------------------------

        try:

            result = ask_agent(
                question=question,
                thread_id=thread_id,
            )

        except Exception as error:

            print("\n" + "=" * 80)
            print("AGENT ERROR")
            print("=" * 80)
            print(str(error))

            continue

        # ----------------------------------------------------
        # DEBUG
        # ----------------------------------------------------

        print_tool_calls(result)

        # ----------------------------------------------------
        # ANSWER
        # ----------------------------------------------------

        answer = get_final_answer(result)

        print("\n" + "=" * 80)
        print("AGENT")
        print("=" * 80)

        print(answer)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()