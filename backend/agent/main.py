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

import uuid

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
)

from backend.agent.graph import graph


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_THREAD_ID = "amine-session-001"


# ============================================================
# ASK AGENT
# ============================================================

def ask_agent(
    question: str,
    thread_id: str = DEFAULT_THREAD_ID,
):
    """
    Send a question to the LangGraph agent.

    The thread_id identifies the conversation.
    PostgreSQL uses it to restore the previous state.
    """

    question = question.strip()

    if not question:
        raise ValueError(
            "Question cannot be empty."
        )

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
                    content=question
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

    Tool-call AI messages are ignored until a final
    textual response is available.
    """

    messages = result.get(
        "messages",
        [],
    )

    if not messages:
        return "No response was generated."

    for message in reversed(messages):

        if not isinstance(
            message,
            AIMessage,
        ):
            continue

        # ----------------------------------------------------
        # Ignore AI messages that only contain tool calls
        # ----------------------------------------------------

        tool_calls = getattr(
            message,
            "tool_calls",
            [],
        )

        if tool_calls:
            continue

        content = message.content

        # ----------------------------------------------------
        # Normal string response
        # ----------------------------------------------------

        if isinstance(
            content,
            str,
        ):

            content = content.strip()

            if content:
                return content

        # ----------------------------------------------------
        # Handle structured content
        # ----------------------------------------------------

        if isinstance(
            content,
            list,
        ):

            text_parts = []

            for block in content:

                if isinstance(
                    block,
                    dict,
                ):

                    text = block.get(
                        "text"
                    )

                    if text:
                        text_parts.append(
                            str(text)
                        )

            if text_parts:

                return "\n".join(
                    text_parts
                ).strip()

    return (
        "The agent did not generate "
        "a final answer."
    )


# ============================================================
# DEBUG TOOL CALLS
# ============================================================

def print_tool_calls(result):
    """
    Display tools called during the request.

    Useful during development and debugging.
    """

    messages = result.get(
        "messages",
        [],
    )

    tool_calls_found = False

    for message in messages:

        # ----------------------------------------------------
        # AI tool calls
        # ----------------------------------------------------

        if isinstance(
            message,
            AIMessage,
        ):

            tool_calls = getattr(
                message,
                "tool_calls",
                [],
            )

            for call in tool_calls:

                tool_calls_found = True

                name = call.get(
                    "name",
                    "unknown",
                )

                args = call.get(
                    "args",
                    {},
                )

                print(
                    f"\n[Tool Call] {name}"
                )

                print(
                    f"[Arguments] {args}"
                )

        # ----------------------------------------------------
        # Tool results
        # ----------------------------------------------------

        elif isinstance(
            message,
            ToolMessage,
        ):

            tool_calls_found = True

            print(
                f"\n[Tool Result] "
                f"{message.name}"
            )

    return tool_calls_found


# ============================================================
# NEW CONVERSATION
# ============================================================

def create_new_thread():
    """
    Create a new conversation thread.
    """

    return f"amine-{uuid.uuid4()}"


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

    print(
        "Memory: PostgreSQL"
    )

    print("\nCommands:")
    print(
        "  /new  → start a new conversation"
    )
    print(
        "  /exit → quit"
    )

    while True:

        try:

            question = input(
                "\nYou: "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError,
        ):

            print(
                "\nGoodbye!"
            )

            break

        if not question:
            continue

        # ====================================================
        # EXIT
        # ====================================================

        if question.lower() in {
            "/exit",
            "/quit",
            "exit",
            "quit",
        }:

            print(
                "\nGoodbye!"
            )

            break

        # ====================================================
        # NEW CONVERSATION
        # ====================================================

        if question.lower() == "/new":

            thread_id = create_new_thread()

            print(
                "\nNew conversation started."
            )

            print(
                f"Thread ID: {thread_id}"
            )

            continue

        # ====================================================
        # RUN AGENT
        # ====================================================

        try:

            result = ask_agent(
                question=question,
                thread_id=thread_id,
            )

        except Exception as error:

            print(
                "\n" + "=" * 80
            )

            print(
                "AGENT ERROR"
            )

            print(
                "=" * 80
            )

            print(
                str(error)
            )

            continue

        # ====================================================
        # DEBUG
        # ====================================================

        print_tool_calls(
            result
        )

        # ====================================================
        # FINAL ANSWER
        # ====================================================

        answer = get_final_answer(
            result
        )

        print(
            "\n" + "=" * 80
        )

        print(
            "AGENT"
        )

        print(
            "=" * 80
        )

        print(
            answer
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()